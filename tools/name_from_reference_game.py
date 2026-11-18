"""Name this game's SDK functions after another game that has the same code.

Nombra las funciones del SDK de este juego con las de otro juego que tenga el mismo código.

Dolphin's signature database leaves out short functions and functions whose checksum several share, and
this game's SDK is older than most of what the database was built from. The Harvest Moon: Animal Parade
port named many of those by hand. Where a function there has exactly the same code as an unnamed one
here (with branch targets and address halves masked out, as tools/port_addresses.py compares them), it
gets the same name. Two unnamed functions with the same code are told apart by their neighbours, since
the linker keeps the functions of one SDK source file together; when that does not settle it, the
function is left unnamed.

La base de firmas de Dolphin deja fuera funciones cortas y las de checksum compartido, y el SDK de este
juego es más viejo que casi todo lo que hay en ella. El port de Animal Parade nombró muchas a mano. Si una
función de allá tiene exactamente el mismo código que una sin nombre de aquí, recibe el mismo nombre;
dos iguales se distinguen por sus vecinas, y si eso no basta, se queda sin nombre.

Only names of the Nintendo SDK are carried over (tools/sdk_libraries.py knows their prefixes): the
game's own code shares nothing with another game.

Usage / Uso:
    python3 tools/name_from_reference_game.py --reference-dol ../AnimalParade/orig/RBIEE9/sys/main.dol \\
        --reference-symbols ../AnimalParade/config/RBIEE9/symbols.txt            # lists
    python3 tools/name_from_reference_game.py ... --apply                        # writes symbols.txt
"""

import argparse
import sys
from dataclasses import replace
from pathlib import Path

from port_addresses import Game, same_code
from project import MAIN_DOL_PATH, SYMBOLS_PATH
from sdk_libraries import library_of


def names_to_carry(reference: Game, target: Game) -> dict[int, str]:
    """{address here: name} for the SDK functions found by their code."""
    taken = {symbol.name for symbol in target.symbols}
    found: dict[int, str] = {}
    for symbol in reference.symbols:
        if symbol.kind != "function" or symbol.has_generated_name or symbol.name in taken:
            continue
        if not library_of(symbol.name):
            continue
        here = same_code(reference, symbol, target)
        if here is not None and here.has_generated_name and here.address not in found:
            found[here.address] = symbol.name
    # A name that two functions here would take names neither.
    counts: dict[str, int] = {}
    for name in found.values():
        counts[name] = counts.get(name, 0) + 1
    return {address: name for address, name in found.items() if counts[name] == 1}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--reference-dol", type=Path, required=True, help="the other game's main.dol")
    parser.add_argument("--reference-symbols", type=Path, required=True, help="its symbols.txt")
    parser.add_argument("--dol", type=Path, default=MAIN_DOL_PATH)
    parser.add_argument("--symbols", type=Path, default=SYMBOLS_PATH)
    parser.add_argument("--apply", action="store_true", help="write the names into symbols.txt")
    arguments = parser.parse_args()

    reference = Game.load(arguments.reference_dol, arguments.reference_symbols)
    target = Game.load(arguments.dol, arguments.symbols)
    found = names_to_carry(reference, target)
    for address, name in sorted(found.items()):
        print(f"0x{address:08X}  {name}")
    print(f"{len(found)} SDK functions named by their code", file=sys.stderr)
    if arguments.apply and found:
        for address, name in found.items():
            target.symbols.add(replace(target.symbols.by_address[address], name=name, scope="global"))
        target.symbols.write(arguments.symbols)
    return 0


if __name__ == "__main__":
    sys.exit(main())
