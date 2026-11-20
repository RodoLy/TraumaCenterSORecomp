"""Find where the game's control instructions sit, for the control texts mod.

Some tutorial lines name the Wii Remote's buttons ("(A and B Buttons)", "(Z Button)"). The port
rewrites those lines for the control mode the player chose (mouse, mouse and keyboard, mouse and
controller); see runtime/src/hle/game_mods/trauma_center_control_texts.cpp. This tool finds each of
those lines on the disc and prints, for the C++ table, where the line starts in its file, how long it
is and a hash of it, so the port can check it rewrites the right bytes. The game's own text is never
copied: the table holds positions, lengths and hashes, and only our new lines are written out.

A new line replaces an old one in place and may not be longer than it; a shorter one is padded with
spaces. That keeps every file exactly the size it was.

Usage:
    python tools/control_texts.py <disc>/files

Files: operation/msg_ope.pak (operation dialogue, a pack of MSG2 files) and
storyflow/msg/explanation_eng.bm2 (one MSG2 file).

MSG2 layout, as far as this tool needs it (big-endian):
    0x04  'MSG2'
    0x28  number of messages
    0x2C  where the message table starts (0x30, or later when a table of speaker names comes first)
    table one 0x40-byte entry per message: name (0x24 bytes), size, offset from the file's start
Inside a message, each line of text is a run of printable characters ending in a zero byte; the
commands between lines start with 0xFF. Lines are counted from 0 in the order they appear.

A .pak is a row of files, each with a 0x100-byte header (name in the first 0xFC bytes, then the size
as a little-endian 32-bit number) and its data, every file starting on a 0x40-byte boundary.
"""

from __future__ import annotations

import re
import struct
import sys
from pathlib import Path

# (file, message, line) -> what a line says on each control mode. None keeps the original line.
# Line numbers count the message's lines from 0.
REWRITES = [
    # Forceps: "...by pressing with / both fingers (A and B Buttons)."
    ("operation/msg_ope.pak", "MSG_OPE101_SELECT_FORCEPS", 0,
     "Grip the glass fragments by holding down", "Grip the glass fragments by holding down", None),
    ("operation/msg_ope.pak", "MSG_OPE101_SELECT_FORCEPS", 1,
     "the left button for a moment.", "Space, or the left button.", None),
    # Ultrasound: "...by pressing / the B Button."
    ("operation/msg_ope.pak", "MSG_OPE102_SELECT_ULTRASOUND", 0,
     "You can activate the ultrasound with the", "You can activate the ultrasound with", None),
    ("operation/msg_ope.pak", "MSG_OPE102_SELECT_ULTRASOUND", 1,
     "right button.", "Left Shift.", None),
    # Magnifier: "press the A Button to activate it."
    ("operation/msg_ope.pak", "MSG_OPE105_SELECT_MAGNIFICATION", 1,
     "click to activate it.", "click to activate it.", None),
    # Defibrillator: "...press / the B Button and Z Button simultaneously."
    ("operation/msg_ope.pak", "MSG_OPE108_STEP_1ST_DEFIBRILLAT", 17,
     "and hold the right mouse button down.", "Left Shift and Q at the same time.",
     "the B Button and LT (L2) together."),
    # Healing Touch: Z first ("tensed my index finger (Z Button)"), then B, then a star.
    ("operation/msg_ope.pak", "MSG_OPE203_START_OPE", 4,
     "Let's see... I think I held down", None, None),
    ("operation/msg_ope.pak", "MSG_OPE203_START_OPE", 5,
     "the right button...", "index finger...(Q key)", "index finger...(LT / L2)"),
    ("operation/msg_ope.pak", "MSG_OPE203_KEEP_Z", 1,
     "Kept it held down... (right button)", "Tense my other hand... (Left Shift)", None),
    ("operation/msg_ope.pak", "MSG_OPE203_CAUTION_Z_RELEASE", 1, "(hold it)", "(Q key)", "(LT / L2)"),
    ("operation/msg_ope.pak", "MSG_OPE203_CAUTION_Z_RELEASE", 3, "(hold it)", "(Q key)", "(LT / L2)"),
    ("operation/msg_ope.pak", "MSG_OPE203_CAUTION_B_RELEASE", 2, "(hold it)", "(L. Shift)", None),
    # Episode menu: "You can also select your difficulty / mode with the Z or C Buttons."
    ("storyflow/msg/explanation_eng.bm2", "LABEL01", 2,
     "Middle or side mouse button changes", None, None),
    ("storyflow/msg/explanation_eng.bm2", "LABEL01", 3,
     "the difficulty mode.", "mode with the Q or E keys.", "mode with LT or RT (L2/R2)."),
]

LINE = re.compile(rb"[\x20-\x7e]{2,}(?=\x00)")


def fnv1a(data: bytes) -> int:
    value = 0x811C9DC5
    for byte in data:
        value = ((value ^ byte) * 0x01000193) & 0xFFFFFFFF
    return value


def pak_files(data: bytes):
    """(name, start, size) for every file in a .pak."""
    position = 0
    while position + 0x100 <= len(data):
        name = data[position:position + 0xFC].split(b"\0")[0].decode()
        if not name:
            return
        size = struct.unpack_from("<I", data, position + 0xFC)[0]
        yield name, position + 0x100, size
        position = (position + 0x100 + size + 0x3F) & ~0x3F


def messages(data: bytes, start: int):
    """(name, start, size) for every message of the MSG2 file at `start`."""
    if data[start + 4:start + 8] != b"MSG2":
        raise ValueError("not an MSG2 file")
    count, table = struct.unpack_from(">II", data, start + 0x28)
    for index in range(count):
        entry = start + table + index * 0x40
        name = data[entry:entry + 0x24].split(b"\0")[0].decode("ascii", "replace")
        size, offset = struct.unpack_from(">II", data, entry + 0x24)
        yield name, start + offset, size


def find_line(data: bytes, message: str, line: int) -> tuple[int, int]:
    """Where a message's line starts in the file, and its length."""
    starts = [start for _, start, _ in pak_files(data)] if data[4:8] != b"MSG2" else [0]
    # Names longer than the entry's 0x24 bytes are cut short, so one name can stand for a few
    # messages in a row; their lines are counted together, in order.
    lines = []
    for file_start in starts:
        for name, start, size in messages(data, file_start):
            if name == message:
                lines += list(LINE.finditer(data, start, start + size))
    if line >= len(lines):
        raise KeyError(f"{message} line {line}")
    found = lines[line]
    return found.start(), found.end() - found.start()


def main() -> None:
    root = Path(sys.argv[1])
    cache: dict[str, bytes] = {}
    print("// Generated by tools/control_texts.py: file, offset, length, FNV-1a of the original line,")
    print("// then the line for mouse, for mouse and keyboard, and for mouse and controller.")
    for file, message, line, mouse, keys, controller in REWRITES:
        data = cache.setdefault(file, (root / file).read_bytes())
        offset, length = find_line(data, message, line)
        for text in (mouse, keys, controller):
            if text is not None and len(text) > length:
                raise SystemExit(f"{message} line {line}: '{text}' is longer than the {length} it replaces")
        quoted = ", ".join("nullptr" if text is None else f'"{text}"' for text in (mouse, keys, controller))
        hashed = fnv1a(data[offset:offset + length])
        print(f'    {{"{Path(file).name}", {offset}, {length}, 0x{hashed:08X}u, {{{quoted}}}}}, '
              f"// {message} line {line}")


if __name__ == "__main__":
    main()
