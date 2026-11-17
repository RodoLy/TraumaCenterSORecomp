"""RVZ reader tests on a tiny disc image built by hand, so no game data is needed.

Pruebas del lector de RVZ con una imagen de disco mínima hecha a mano, sin datos del juego.

The image has one partition of two groups. The first group is stored as is; the second is
compressed with zstd and packed, with a run of junk at its start, like Dolphin writes them.

La imagen tiene una partición de dos grupos. El primero se guarda tal cual; el segundo va
comprimido con zstd y empaquetado, con un tramo de basura al principio, como los escribe
Dolphin.
"""

import struct
import sys
from pathlib import Path

import pytest
import zstandard

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import extract_system_files  # noqa: E402
import rvz  # noqa: E402

CHUNK_SIZE = 0x10000  # two sectors per group, to keep the image small
GROUP_DATA_SIZE = 2 * rvz.SECTOR_DATA_SIZE
FIRST_SECTOR = 0x10
JUNK_SIZE = 0x100


def partition_data() -> bytes:
    """Two groups of data: a boot.bin pointing at a small DOL and a file table."""
    data = bytearray(2 * GROUP_DATA_SIZE)
    data[:6] = b"RKDEEB"
    dol_offset = GROUP_DATA_SIZE + JUNK_SIZE  # the DOL sits in the second group, after junk
    fst_offset = 0x1000
    struct.pack_into(">III", data, rvz.DOL_OFFSET_AT, dol_offset >> 2, fst_offset >> 2, 0x40 >> 2)
    data[fst_offset : fst_offset + 0x40] = bytes(range(0x40))

    dol = bytearray(0x100 + 0x20)
    struct.pack_into(">I", dol, 0x00, 0x100)  # text0 file offset
    struct.pack_into(">I", dol, 0x48, 0x80003100)  # text0 address
    struct.pack_into(">I", dol, 0x90, 0x20)  # text0 size
    dol[0x100:] = b"\x4e\x80\x00\x20" * 8  # blr
    data[dol_offset : dol_offset + len(dol)] = dol
    return bytes(data)


def build_rvz(data: bytes) -> bytes:
    no_exceptions = b"\x00\x00"
    first = no_exceptions + b"\x00\x00" + data[:GROUP_DATA_SIZE]  # padded to 4 bytes
    second_data = data[GROUP_DATA_SIZE:]
    packed = (
        struct.pack(">I", rvz.JUNK_FLAG | JUNK_SIZE)
        + bytes(rvz.JUNK_SEED_SIZE)
        + struct.pack(">I", GROUP_DATA_SIZE - JUNK_SIZE)
        + second_data[JUNK_SIZE:]
    )
    second = zstandard.ZstdCompressor().compress(no_exceptions + packed)

    # The tables fit easily in the first 0x400 bytes; the groups go after them.
    first_offset = 0x400
    second_offset = (first_offset + len(first) + 3) & ~3

    disc_struct_size = 0x10 + rvz.DISC_HEAD_SIZE + 16 + 20 + 32
    partitions_offset = rvz.FILE_HEAD_SIZE + disc_struct_size
    partition_entry = bytes(16) + struct.pack(">IIII", FIRST_SECTOR, 2, 0, 1)
    partition_entry += struct.pack(">IIII", FIRST_SECTOR + 2, 2, 1, 1)
    groups_offset = partitions_offset + len(partition_entry)
    groups = zstandard.ZstdCompressor().compress(
        struct.pack(">III", first_offset // 4, len(first), 0)
        + struct.pack(">III", second_offset // 4, rvz.GROUP_COMPRESSED_FLAG | len(second), len(packed))
    )

    disc_head = data[:6] + bytes(rvz.DISC_HEAD_SIZE - 6)
    disc = struct.pack(">IIiI", rvz.DISC_TYPE_WII, rvz.COMPRESSION_ZSTD, 5, CHUNK_SIZE)
    disc += disc_head
    disc += struct.pack(">IIQ", 1, len(partition_entry), partitions_offset) + bytes(20)
    disc += struct.pack(">IQIIQI", 0, 0, 0, 2, groups_offset, len(groups))

    head = bytearray(rvz.FILE_HEAD_SIZE)
    head[:4] = rvz.MAGIC
    struct.pack_into(">I", head, 0x0C, len(disc))

    image = bytearray(head + disc + partition_entry + groups)
    image += bytes(first_offset - len(image)) + first
    image += bytes(second_offset - len(image)) + second
    return bytes(image)


@pytest.fixture
def disc() -> rvz.RvzDisc:
    image = build_rvz(partition_data())
    return rvz.RvzDisc(lambda offset, size: image[offset : offset + size])


def test_reads_across_a_stored_and_a_compressed_packed_group(disc):
    data = partition_data()
    start = GROUP_DATA_SIZE - 0x10
    assert disc.read_partition(0, start, 0x10) == data[start:GROUP_DATA_SIZE]
    after_junk = GROUP_DATA_SIZE + JUNK_SIZE
    assert disc.read_partition(0, after_junk, 0x40) == data[after_junk : after_junk + 0x40]


def test_reading_junk_is_refused(disc):
    with pytest.raises(rvz.JunkDataError):
        disc.read_partition(0, GROUP_DATA_SIZE, 0x10)


def test_extracts_boot_dol_and_file_table(disc):
    files = extract_system_files.system_files(disc)

    assert files["boot.bin"][:6] == b"RKDEEB"
    assert len(files["main.dol"]) == 0x120
    assert files["main.dol"][0x100:0x104] == b"\x4e\x80\x00\x20"
    assert files["fst.bin"] == bytes(range(0x40))


def test_other_files_are_refused():
    with pytest.raises(ValueError, match="not an RVZ"):
        rvz.RvzDisc(lambda offset, size: bytes(size))
