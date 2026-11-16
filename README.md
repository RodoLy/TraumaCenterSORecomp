# Trauma Center: Second Opinion – native PC port

[Español](README.es.md)

A native PC port of *Trauma Center: Second Opinion* (Wii) by static recompilation, in the works:
the game's PowerPC code will be translated to C++ and compiled for your computer, with no
emulator. It follows the same path as the
[*Harvest Moon: Animal Parade* port](https://github.com/RodoLy/HarvestMoonAnimalParadeRecomp).

> **Early days.** Nothing is playable yet. This repository holds the analysis tools and the plan
> ([docs/PLAN.md](docs/PLAN.md)). The first step is the function map of the game.

**This repository contains no game data.** You need your own disc: `Trauma Center: Second
Opinion (USA)`, ID `RKDEEB`.

## Planned

- Native on Windows x64 and Windows on ARM.
- No Wii Remote needed: the mouse is the pointer, and the Nunchuk goes to a gamepad or the
  keyboard.
- High resolution and an optional widescreen mod (the original game is 4:3 only).
- Out of the box, everything looks and plays as it did on the Wii.

## Phase 0: map the game's functions

What you need: Python 3.11 or newer, and your disc extracted with
[Dolphin](https://dolphin-emu.org/) (right click on the game > *Properties* > *Filesystem* >
right click on the disc > *Extract Entire Disc…*) or with Wiimms ISO Tools (`wit`).

1. Install the tools' dependencies:

   ```sh
   pip install -r requirements-dev.txt
   ```

2. Put the extracted game partition in `orig/RKDEEB/`, so that `orig/RKDEEB/sys/main.dol` and
   `orig/RKDEEB/sys/boot.bin` exist. Nothing in `orig/` is ever committed.

3. Check the disc:

   ```sh
   python3 tools/check_disc.py
   ```

   The first time, it prints the revision and the SHA-1 of `main.dol`. Write them as
   `EXPECTED_REVISION` and `EXPECTED_DOL_SHA1` in `tools/check_disc.py`, so later checks compare
   against them.

4. Build the function map:

   ```sh
   python3 tools/analyze.py
   ```

   It writes `config/RKDEEB/symbols.txt`, the single list of function names and sizes that every
   other tool reads.

5. Run the tests at any time with `python3 -m pytest`. They build tiny DOL files by hand, so they
   need no game data.

## Thanks

- [WiiCompiled](https://github.com/patchzyy/wiicompiled) and
  [ModernGekko](https://github.com/ExpansionPak/ModernGekko-Template) with DolRecomp, the
  recompilation tools this port is built on.
- [aurora](https://github.com/encounter/aurora) and [decomp-toolkit](https://github.com/encounter/decomp-toolkit).
- Atlus, for the game. This is an unofficial fan project, not affiliated with or endorsed by
  Atlus, Sega or Nintendo.

## License

GPL-3.0 (see [LICENSE](LICENSE)). The license covers this repository's code only; it grants
nothing for the game.
