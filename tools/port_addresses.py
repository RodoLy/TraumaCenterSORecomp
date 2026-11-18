"""Carry an address table from another game's port over to this game, by comparing the SDK code.

Pasa una tabla de direcciones del port de otro juego a este, comparando el código del SDK.

WiiCompiled's native runtime looks for SDK functions and variables at Mario Kart Wii's addresses. The
Harvest Moon: Animal Parade port already wrote, for each of them, where Animal Parade keeps it and the
evidence: the function's name, or the function that reads or writes the variable
(wiicompiled/RBIEE9-*-addresses.txt in that repository). Both games use the same Nintendo SDK, so the
same evidence finds the same things here:

- a function row: symbols.txt of this game has a function with that name; when the signature database
  did not name it, the function with the same code is taken, and its name is added to symbols.txt;
- a variable row: the evidence function, found here by its name, reaches its variables in the same order
  as in Animal Parade, so the n-th address it reaches there is the n-th one it reaches here. When the two
  functions do not reach the same number of addresses they were built differently, and the row is left
  for a person ("?").

La tabla del otro juego dice, para cada cosa, dónde la guarda Animal Parade y la evidencia. Como los dos
juegos usan el mismo SDK de Nintendo, la misma evidencia la encuentra aquí: una función por su nombre (o,
si la base de firmas no la nombró, la función con el mismo código, cuyo nombre se agrega a symbols.txt), y
una variable por el orden en que la alcanza la función de la evidencia. Si esa función alcanza un número
distinto de direcciones en los dos juegos, se compiló distinto y la fila queda para una persona ("?").

Every row written here is checked again by tests/test_wiicompiled_addresses.py against this game's
main.dol, so a wrong guess cannot slip through.

Cada fila escrita aquí la vuelve a comprobar tests/test_wiicompiled_addresses.py contra el main.dol de este
juego, así que una suposición equivocada no puede colarse.

Usage / Uso:
    python3 tools/port_addresses.py --reference-dol ../AnimalParade/orig/RBIEE9/sys/main.dol \\
        --reference-symbols ../AnimalParade/config/RBIEE9/symbols.txt \\
        ../AnimalParade/wiicompiled/RBIEE9-os-addresses.txt > wiicompiled/RKDEEB-os-addresses.txt
"""

import argparse
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass, replace
from pathlib import Path
from struct import unpack

from code_facts import REGISTERS_A_CALL_MAY_CHANGE, WORD_MASK, _address_put_together_by
from dol import Dol
from function_finder import INSTRUCTION_SIZE, find_small_data_bases
from ppc import MEMORY_OPCODES, Instruction
from project import GAME_ID, MAIN_DOL_PATH, SYMBOLS_PATH
from symbols import Symbol, SymbolTable

COLUMNS = re.compile(r"\s{2,}")
# Instructions whose low 16 bits are an address part or an offset that moves from game to game:
# addi, addis, ori, the compares' neighbours aside, and every load and store.
# Instrucciones cuyos 16 bits bajos son parte de una dirección o un desplazamiento que cambia de juego
# a juego.
OPCODES_WITH_A_MOVING_IMMEDIATE = {14, 15, 24, *range(32, 56)}
OPCODE_BRANCH = 18  # b, bl: the target moves with the code
OPCODE_BRANCH_CONDITIONAL = 16
FUNCTION_EVIDENCE = "name"
ENTRY_POINT = "entry point"
HELD_AT = "held at "
# A row this tool could not port: "?" in column 2, and "? why" in column 4.
UNKNOWN = "?"


@dataclass
class Game:
    dol: Dol
    symbols: SymbolTable
    small_data_bases: Mapping[int, int]

    @classmethod
    def load(cls, dol_path: Path, symbols_path: Path) -> "Game":
        dol = Dol(dol_path)
        return cls(dol, SymbolTable.read(symbols_path), find_small_data_bases(dol))

    def function(self, name: str) -> Symbol | None:
        return self.symbols.by_name(name)

    def shape(self, function: Symbol) -> tuple[int, ...]:
        """The function's code with what moves between games masked out: branch targets, and the
        immediates of address parts, loads and stores."""
        count = function.size // INSTRUCTION_SIZE
        words = unpack(f">{count}I", self.dol.read(function.address, function.size))
        shape = []
        for word in words:
            opcode = word >> 26
            if opcode == OPCODE_BRANCH:
                word &= 0xFC000003
            elif opcode in OPCODES_WITH_A_MOVING_IMMEDIATE:
                word &= 0xFFFF0000
            shape.append(word)
        return tuple(shape)


def same_code(reference: Game, function: Symbol, target: Game) -> Symbol | None:
    """The one function of the target with the same code shape as `function`, or None.

    A function that already has another name is not a candidate: SCGetProductArea and
    SCGetProductGameRegion have the same code, reading two different tables. When several unnamed ones
    have it (small helpers often do), the one whose neighbours have the same names as in the reference
    game is taken, since the linker keeps a source file's functions together."""
    wanted = reference.shape(function)
    candidates = [
        symbol
        for symbol in target.symbols
        if symbol.kind == "function"
        and (symbol.has_generated_name or symbol.name == function.name)
        and symbol.size == function.size
        and target.shape(symbol) == wanted
    ]
    if len(candidates) == 1:
        return candidates[0]
    neighbours_there = _neighbour_names(reference, function)
    matching = [c for c in candidates if _neighbour_names(target, c) & neighbours_there]
    return matching[0] if len(matching) == 1 else None


def _neighbour_names(game: Game, function: Symbol) -> set[str]:
    names = set()
    for address in (function.address - INSTRUCTION_SIZE, function.address + function.size):
        neighbour = game.symbols.containing(address)
        if neighbour is not None and not neighbour.has_generated_name:
            names.add(neighbour.name)
    return names


def find_function(reference: Game, target: Game, name: str, names_found: dict[int, str]) -> Symbol | None:
    """This game's function called `name` in the reference game, by name or else by its code.

    `name` may also be a bare address (0x8025AB90), as the tables write an unnamed function. A function
    found by its code is noted in `names_found` ({address: name}) so symbols.txt can be given the name."""
    found = target.function(name)
    if found is not None:
        return found
    there = reference.symbols.containing(int(name, 16)) if name.startswith("0x") else reference.function(name)
    if there is None:
        return None
    found = same_code(reference, there, target)
    if found is not None and not name.startswith("0x") and found.has_generated_name:
        names_found[found.address] = name
    return found


def addresses_in_order(game: Game, function: Symbol) -> list[int]:
    """The addresses `function` puts together or reads and writes at, in the order it first reaches them.

    The same register following as tools/code_facts.py, keeping the order instead of a set."""
    count = function.size // INSTRUCTION_SIZE
    words = unpack(f">{count}I", game.dol.read(function.address, function.size))
    known: dict[int, int] = dict(game.small_data_bases)
    reached: list[int] = []

    def reach(address: int) -> None:
        if address not in reached:
            reached.append(address)

    for index, word in enumerate(words):
        instruction = Instruction(function.address + index * INSTRUCTION_SIZE, word)
        if instruction.opcode in MEMORY_OPCODES and instruction.ra in known:
            reach((known[instruction.ra] + instruction.displacement) & WORD_MASK)
        address = _address_put_together_by(instruction, known)
        for register in instruction.written_registers:
            known.pop(register, None)
        if instruction.is_call:
            for register in REGISTERS_A_CALL_MAY_CHANGE:
                known.pop(register, None)
        if address is not None:
            destination = instruction.ra if instruction.is_or_immediate else instruction.rd
            known[destination] = address
            if not instruction.is_load_immediate_shifted:
                reach(address)
    return [address for address in reached if address not in game.small_data_bases.values()]


def port_row(row: list[str], reference: Game, target: Game, names_found: dict[int, str]) -> tuple[str, str]:
    """This game's address for one table row and its evidence, or "?" and why it was not found."""
    reference_address, what, evidence = row[1], row[2], row[3]
    if reference_address == "-":
        return "-", evidence
    if evidence == FUNCTION_EVIDENCE:
        name = what.split()[0]
        found = find_function(reference, target, name, names_found)
        return (f"0x{found.address:08X}", evidence) if found else (UNKNOWN, f"no function like {name}")
    if evidence == ENTRY_POINT:
        return f"0x{target.dol.entry:08X}", evidence
    if evidence.startswith(HELD_AT):
        return UNKNOWN, "held in a data word: find the word by hand"

    evidence_name = evidence.split()[0]
    there = (
        reference.symbols.containing(int(evidence_name, 16))
        if evidence_name.startswith("0x")
        else reference.function(evidence_name)
    )
    here = find_function(reference, target, evidence_name, names_found)
    if there is None or here is None:
        return UNKNOWN, f"no function like {evidence_name}"
    reached_there = addresses_in_order(reference, there)
    reached_here = addresses_in_order(target, here)
    address = int(reference_address, 16)
    if address not in reached_there:
        return UNKNOWN, f"{evidence_name} does not reach it in the reference game"
    if len(reached_there) != len(reached_here):
        return UNKNOWN, (
            f"{evidence_name} reaches {len(reached_there)} addresses there and {len(reached_here)} here"
        )
    # An unnamed function is written by its address, which is this game's one from now on.
    evidence_here = f"0x{here.address:08X}" if evidence_name.startswith("0x") else evidence
    return f"0x{reached_here[reached_there.index(address)]:08X}", evidence_here


def port_table(
    text: str, reference: Game, target: Game, reference_id: str, names_found: dict[int, str]
) -> tuple[str, int, int]:
    """The table with this game's addresses in column 2; also how many rows were ported and left."""
    lines, ported, left = [], 0, 0
    for line in text.splitlines():
        if not line.startswith("0x"):
            lines.append(line.replace(reference_id, GAME_ID))
            continue
        row = COLUMNS.split(line.strip(), maxsplit=3)
        address, evidence = port_row(row, reference, target, names_found)
        if address == UNKNOWN:
            left += 1
            evidence = f"{UNKNOWN} {evidence}"
        elif address != "-":
            ported += 1
        lines.append(f"{row[0]}  {address:<10}  {row[2]:<46}  {evidence}")
    return "\n".join(lines) + "\n", ported, left


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("table", type=Path, help="the other game's table (RBIEE9-*-addresses.txt)")
    parser.add_argument("--reference-dol", type=Path, required=True, help="the other game's main.dol")
    parser.add_argument("--reference-symbols", type=Path, required=True, help="its symbols.txt")
    parser.add_argument("--reference-id", default="RBIEE9", help="its game ID (default: RBIEE9)")
    parser.add_argument("--dol", type=Path, default=MAIN_DOL_PATH)
    parser.add_argument("--symbols", type=Path, default=SYMBOLS_PATH)
    parser.add_argument(
        "--apply-names",
        action="store_true",
        help="give symbols.txt the names of the functions found by their code",
    )
    arguments = parser.parse_args()

    reference = Game.load(arguments.reference_dol, arguments.reference_symbols)
    target = Game.load(arguments.dol, arguments.symbols)
    names_found: dict[int, str] = {}
    text, ported, left = port_table(
        arguments.table.read_text(encoding="utf-8"),
        reference,
        target,
        arguments.reference_id,
        names_found,
    )
    sys.stdout.write(text)
    print(f"{arguments.table.name}: {ported} rows ported, {left} left for a person", file=sys.stderr)
    for address, name in sorted(names_found.items()):
        print(f"  found by its code: {name} at 0x{address:08X}", file=sys.stderr)
    if arguments.apply_names and names_found:
        for address, name in names_found.items():
            old = target.symbols.by_address[address]
            target.symbols.add(replace(old, name=name, scope="global"))
        target.symbols.write(arguments.symbols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
