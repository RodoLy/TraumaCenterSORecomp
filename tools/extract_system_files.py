"""Pull the game's system files out of an RVZ disc image, without Dolphin.

Saca los archivos de sistema del juego de una imagen de disco RVZ, sin Dolphin.

It writes sys/boot.bin (the partition header), sys/main.dol (the program) and sys/fst.bin (the
file table) of the game partition into orig/<game ID>/, which is all that phase 0 needs. The
game ID is read from the disc, so the USA and the European disc land in their own folders.

Escribe sys/boot.bin (la cabecera de la partición), sys/main.dol (el programa) y sys/fst.bin
(la tabla de archivos) de la partición del juego en orig/<ID del juego>/, que es todo lo que
necesita la fase 0. El ID se lee del disco, así que el disco USA y el europeo quedan cada uno
en su carpeta.

Usage / Uso:
    python3 tools/extract_system_files.py "Trauma Center - Second Opinion (USA).rvz"
"""

import argparse
import struct
import sys
from pathlib import Path

import rvz
from project import REPOSITORY_ROOT


def system_files(disc: rvz.RvzDisc) -> dict[str, bytes]:
    partition = disc.game_partition()
    boot = disc.read_partition(partition, 0, rvz.BOOT_SIZE)
    dol_offset = struct.unpack_from(">I", boot, rvz.DOL_OFFSET_AT)[0] << 2
    fst_offset = struct.unpack_from(">I", boot, rvz.FST_OFFSET_AT)[0] << 2
    fst_size = struct.unpack_from(">I", boot, rvz.FST_SIZE_AT)[0] << 2

    dol_header = disc.read_partition(partition, dol_offset, 0x100)
    return {
        "boot.bin": boot,
        "main.dol": disc.read_partition(partition, dol_offset, rvz.dol_size(dol_header)),
        "fst.bin": disc.read_partition(partition, fst_offset, fst_size),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("image", type=Path, help="the .rvz disc image")
    parser.add_argument(
        "--out",
        type=Path,
        default=REPOSITORY_ROOT / "orig",
        help="where the <game ID>/sys folder is created (default: orig/)",
    )
    arguments = parser.parse_args()

    disc = rvz.RvzDisc(rvz.file_reader(arguments.image))
    game_id = disc.disc_head[:6].decode("ascii")
    sys_directory = arguments.out / game_id / "sys"
    sys_directory.mkdir(parents=True, exist_ok=True)

    for name, data in system_files(disc).items():
        (sys_directory / name).write_bytes(data)
        print(f"{game_id}/sys/{name:9} {len(data):#10x} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
