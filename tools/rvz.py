"""Read files from the game partition of a Wii disc image in RVZ format.

Lee archivos de la partición del juego de una imagen de disco de Wii en formato RVZ.

RVZ is Dolphin's compressed disc format (a variant of WIA). This reader only does what the
port needs: find the game partition and read bytes from its (already decrypted) data, so that
tools/extract_system_files.py can pull sys/boot.bin, sys/main.dol and friends without Dolphin.
The layout follows Dolphin's own description of the format, docs/WiaAndRvz.md in its source.

RVZ es el formato comprimido de discos de Dolphin (una variante de WIA). Este lector solo hace
lo que necesita el port: encontrar la partición del juego y leer bytes de sus datos (ya
descifrados), para que tools/extract_system_files.py saque sys/boot.bin, sys/main.dol y demás
sin Dolphin. La estructura sigue la descripción del formato que tiene Dolphin en su código,
docs/WiaAndRvz.md.

What it does not do / Lo que no hace:
  - Regenerate "junk" padding (RVZ stores it as a seed, not as bytes). Reading into a junk area
    raises JunkDataError; game files never live there.
    Regenerar el relleno "basura" (RVZ guarda una semilla, no los bytes). Leer en esa zona
    lanza JunkDataError; los archivos del juego nunca están ahí.
  - bzip2/LZMA compression: only zstd and uncompressed groups, which is what Dolphin uses for
    RVZ by default. / Compresión bzip2/LZMA: solo zstd y grupos sin comprimir, lo que Dolphin
    usa para RVZ por defecto.

Every read goes through a `read_at(offset, size)` function, so the bytes can come from the
whole .rvz file or from pieces of it copied from somewhere else.

Cada lectura pasa por una función `read_at(offset, tamaño)`, así los bytes pueden venir del
.rvz entero o de pedazos copiados de otro lado.
"""

import struct
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import zstandard

ReadAt = Callable[[int, int], bytes]

MAGIC = b"RVZ\x01"
FILE_HEAD_SIZE = 0x48
DISC_HEAD_SIZE = 0x80  # the first 0x80 bytes of the disc, kept in the disc struct

DISC_TYPE_WII = 2
COMPRESSION_NONE = 0
COMPRESSION_ZSTD = 5

SECTOR_SIZE = 0x8000  # a Wii sector on disc: 0x400 of hashes + 0x7C00 of data
SECTOR_DATA_SIZE = 0x7C00  # RVZ keeps only the data part of partition sectors
EXCEPTION_SIZE = 2 + 20  # u16 offset + SHA-1 of a hash that differs from the recomputed one

GROUP_COMPRESSED_FLAG = 0x80000000
JUNK_FLAG = 0x80000000
JUNK_SEED_SIZE = 17 * 4

# Offsets inside a partition's boot.bin (the partition header, 0x440 bytes).
BOOT_SIZE = 0x440
DOL_OFFSET_AT = 0x420  # stored shifted right by 2 on Wii
FST_OFFSET_AT = 0x424
FST_SIZE_AT = 0x428


class JunkDataError(Exception):
    """The requested bytes are padding that RVZ stores as a seed."""


@dataclass(frozen=True)
class PartitionRegion:
    first_sector: int
    sector_count: int
    first_group: int
    group_count: int


@dataclass(frozen=True)
class Group:
    file_offset: int
    stored_size: int
    compressed: bool
    packed_size: int


class RvzDisc:
    def __init__(self, read_at: ReadAt):
        self.read_at = read_at
        head = read_at(0, FILE_HEAD_SIZE)
        if head[:4] != MAGIC:
            raise ValueError("not an RVZ file")
        disc_struct_size = struct.unpack_from(">I", head, 0x0C)[0]
        disc = read_at(FILE_HEAD_SIZE, disc_struct_size)

        disc_type, compression, _level, chunk_size = struct.unpack_from(">IIiI", disc, 0)
        if disc_type != DISC_TYPE_WII:
            raise ValueError("only Wii discs are supported")
        if compression not in (COMPRESSION_NONE, COMPRESSION_ZSTD):
            raise ValueError(f"compression {compression} is not supported (only zstd)")
        self.compression = compression
        self.chunk_size = chunk_size
        self.disc_head = disc[0x10 : 0x10 + DISC_HEAD_SIZE]

        at = 0x10 + DISC_HEAD_SIZE
        partition_count, partition_entry_size, partitions_offset = struct.unpack_from(">IIQ", disc, at)
        at += 16 + 20  # skip the SHA-1 of the partition entries
        _raw_count, _raw_offset, _raw_size, group_count, groups_offset, groups_size = struct.unpack_from(
            ">IQIIQI", disc, at
        )

        self.partitions = self._read_partitions(partition_count, partition_entry_size, partitions_offset)
        self.groups = self._read_groups(group_count, groups_offset, groups_size)

    # -- tables ---------------------------------------------------------------------------

    def _read_partitions(self, count, entry_size, offset) -> list[list[PartitionRegion]]:
        table = self.read_at(offset, count * entry_size)
        partitions = []
        for index in range(count):
            entry = table[index * entry_size : (index + 1) * entry_size]
            regions = [
                PartitionRegion(*struct.unpack_from(">IIII", entry, 16 + 16 * part))
                for part in range(2)  # 16 bytes of key, then two data regions
            ]
            partitions.append(regions)
        return partitions

    def _read_groups(self, count, offset, stored_size) -> list[Group]:
        table = self._decompress(self.read_at(offset, stored_size))
        groups = []
        for index in range(count):
            data_offset4, data_size, packed_size = struct.unpack_from(">III", table, index * 12)
            groups.append(
                Group(
                    file_offset=data_offset4 * 4,
                    stored_size=data_size & ~GROUP_COMPRESSED_FLAG,
                    compressed=bool(data_size & GROUP_COMPRESSED_FLAG),
                    packed_size=packed_size,
                )
            )
        return groups

    def _decompress(self, data: bytes) -> bytes:
        if self.compression == COMPRESSION_NONE:
            return data
        return zstandard.ZstdDecompressor().decompress(data, max_output_size=64 << 20)

    # -- partition data -------------------------------------------------------------------

    def game_partition(self) -> int:
        """The game partition is the biggest one (the other is the system update)."""
        sizes = [sum(region.sector_count for region in regions) for regions in self.partitions]
        return sizes.index(max(sizes))

    def read_partition(self, partition: int, offset: int, size: int) -> bytes:
        """Read `size` bytes at `offset` of a partition's decrypted data."""
        sectors_per_group = self.chunk_size // SECTOR_SIZE
        group_data_size = sectors_per_group * SECTOR_DATA_SIZE
        regions = self.partitions[partition]
        first_sector = regions[0].first_sector

        result = bytearray()
        while size > 0:
            sector = first_sector + offset // SECTOR_DATA_SIZE
            region = next(r for r in regions if r.first_sector <= sector < r.first_sector + r.sector_count)
            region_offset = (sector - region.first_sector) * SECTOR_DATA_SIZE + (offset % SECTOR_DATA_SIZE)
            group_index = region.first_group + region_offset // group_data_size
            inside = region_offset % group_data_size
            take = min(size, group_data_size - inside)
            result += self._read_group(group_index, group_data_size, inside, take)
            offset += take
            size -= take
        return bytes(result)

    def _read_group(self, index: int, data_size: int, offset: int, size: int) -> bytes:
        group = self.groups[index]
        if group.stored_size == 0:
            return bytes(size)  # an all-zero group stores nothing
        stored = self.read_at(group.file_offset, group.stored_size)
        data = self._decompress(stored) if group.compressed else stored
        data = data[self._exception_lists_size(data, aligned=not group.compressed) :]
        if group.packed_size:
            data = _unpack(data, offset, offset + size)
        return data[offset : offset + size]

    def _exception_lists_size(self, data: bytes, aligned: bool) -> int:
        """Partition groups start with lists of hash exceptions, one per 2 MiB of data."""
        list_count = max(1, self.chunk_size // 0x200000)
        at = 0
        for _ in range(list_count):
            count = struct.unpack_from(">H", data, at)[0]
            at += 2 + count * EXCEPTION_SIZE
        if aligned:
            at = (at + 3) & ~3
        return at


def _unpack(data: bytes, start: int, end: int) -> bytes:
    """Undo RVZ packing up to `end`: runs of real bytes, and runs of junk stored as a seed.

    Junk before `start` is filled with zeros, since the caller cuts it off anyway.
    """
    out = bytearray()
    at = 0
    while len(out) < end and at < len(data):
        run = struct.unpack_from(">I", data, at)[0]
        at += 4
        length = run & ~JUNK_FLAG
        if run & JUNK_FLAG:
            if len(out) + length > start:
                raise JunkDataError(f"bytes {start:#x}..{end:#x} of a group overlap junk")
            at += JUNK_SEED_SIZE
            out += bytes(length)
        else:
            out += data[at : at + length]
            at += length
    return bytes(out)


def file_reader(path: Path) -> ReadAt:
    handle = open(path, "rb")  # noqa: SIM115 - kept open for the reader's lifetime

    def read_at(offset: int, size: int) -> bytes:
        handle.seek(offset)
        return handle.read(size)

    return read_at


def dol_size(header: bytes) -> int:
    """Size of a DOL from its header: the end of its furthest section."""
    offsets = struct.unpack_from(">18I", header, 0x00)
    sizes = struct.unpack_from(">18I", header, 0x90)
    return max(offset + size for offset, size in zip(offsets, sizes, strict=True) if size)
