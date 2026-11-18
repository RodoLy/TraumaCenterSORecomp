"""Carrying address tables between games, on two hand-built programs.

Pasar tablas de direcciones de un juego a otro, con dos programas hechos a mano.

Both programs have the same three SDK functions, built for different addresses, as two games built
with the same SDK would be:

    VIGetCount   reads one variable                   (named in both games)
    VIInit       reads two variables and stores one   (named in both games)
    OSHelper     the same code as VIGetCount           (named only in the reference game; the target
                 has a function with that code and no name, and an already named lookalike)

Los dos programas tienen las mismas funciones del SDK en direcciones distintas, como dos juegos
compilados con el mismo SDK.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import port_addresses  # noqa: E402
from dol import Dol, write_dol  # noqa: E402
from ppc_encode import BLR, addi, high_adjusted, lis, low, lwz, stw  # noqa: E402
from symbols import Symbol, SymbolTable  # noqa: E402

TEXT = 0x80004000
DATA = 0x80100000


def reads(address: int) -> list[int]:
    return [lis(3, high_adjusted(address)), lwz(3, low(address), 3), BLR]


def build(tmp_path: Path, name: str, variables: list[int], helper_name: str) -> port_addresses.Game:
    """A program with VIGetCount, VIInit, a named lookalike and the helper, in that order."""
    count, first, second = variables
    functions = [
        ("VIGetCount", reads(count)),
        (
            "VIInit",
            [
                lis(4, high_adjusted(first)),
                lwz(5, low(first), 4),
                lis(6, high_adjusted(second)),
                addi(6, 6, low(second)),
                stw(5, 0, 6),
                BLR,
            ],
        ),
        ("SCGetProductArea", reads(count + 0x40)),
        (helper_name, reads(count + 0x80)),
    ]
    words, symbols, address = [], [], TEXT
    for function_name, code in functions:
        symbols.append(Symbol(function_name, ".text", address, "function", len(code) * 4))
        words += code
        address += len(code) * 4
    dol_path = write_dol(
        tmp_path / f"{name}.dol",
        text={0: (TEXT, words)},
        data={0: (DATA, bytes(0x200))},
        entry=TEXT,
    )
    dol = Dol(dol_path)
    return port_addresses.Game(dol, SymbolTable(symbols), {})


def test_a_variable_is_found_by_the_order_its_function_reaches_it(tmp_path):
    reference = build(tmp_path, "reference", [DATA + 0x10, DATA + 0x20, DATA + 0x30], "OSHelper")
    target = build(tmp_path, "target", [DATA + 0x110, DATA + 0x120, DATA + 0x130], "fn_80004030")
    row = ["0x80300000", f"0x{DATA + 0x30:08X}", "the variable VIInit stores", "VIInit"]

    assert port_addresses.port_row(row, reference, target, {}) == (f"0x{DATA + 0x130:08X}", "VIInit")


def test_an_unnamed_function_is_found_by_its_code_and_named(tmp_path):
    reference = build(tmp_path, "reference", [DATA + 0x10, DATA + 0x20, DATA + 0x30], "OSHelper")
    target = build(tmp_path, "target", [DATA + 0x110, DATA + 0x120, DATA + 0x130], "fn_80004030")
    names_found: dict[int, str] = {}
    row = ["0x80300000", "0x80004030", "OSHelper", "name"]

    address, _ = port_addresses.port_row(row, reference, target, names_found)

    assert address == "0x80004030"
    assert names_found == {0x80004030: "OSHelper"}


def test_a_lookalike_with_another_name_is_never_taken(tmp_path):
    reference = build(tmp_path, "reference", [DATA + 0x10, DATA + 0x20, DATA + 0x30], "OSHelper")
    target = build(tmp_path, "target", [DATA + 0x110, DATA + 0x120, DATA + 0x130], "OSOther")
    row = ["0x80300000", "0x80004030", "OSHelper", "name"]

    assert port_addresses.port_row(row, reference, target, {})[0] == port_addresses.UNKNOWN


def test_a_table_keeps_its_comments_and_marks_what_it_could_not_port(tmp_path):
    reference = build(tmp_path, "reference", [DATA + 0x10, DATA + 0x20, DATA + 0x30], "OSHelper")
    target = build(tmp_path, "target", [DATA + 0x110, DATA + 0x120, DATA + 0x130], "OSOther")
    table = (
        "# Where RBIEE9 keeps it\n"
        f"0x80300000  0x{DATA + 0x10:08X}  the count  VIGetCount\n"
        "0x80300004  0x80004030  OSHelper  name\n"
    )

    text, ported, left = port_addresses.port_table(table, reference, target, "RBIEE9", {})

    lines = text.splitlines()
    assert lines[0] == "# Where RKDEEB keeps it"
    assert lines[1].split()[1] == f"0x{DATA + 0x110:08X}"
    assert lines[2].split()[1] == "?"
    assert (ported, left) == (1, 1)
