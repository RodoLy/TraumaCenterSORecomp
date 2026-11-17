# Function map / Mapa de funciones

[Español](#español) · [English](#english)

---

## Español

Primer mapa de `main.dol` del disco USA (`RKDEEB`, revisión 0, SHA-1
`e27a182b057741ce65c16d8789bcf6bdd3d9e52f`). Todo sale de
`config/RKDEEB/symbols.txt`, que se regenera así:

```sh
python3 tools/extract_system_files.py "Trauma Center - Second Opinion (USA).rvz"
python3 tools/analyze.py
python3 tools/sdk_signatures.py --database ruta/a/Dolphin/Sys/totaldb.dsy --apply
```

### Lo que se encontró

| | |
|---|---|
| Funciones | 7802; el código cubre 0x21DA7C de 0x21F4E0 bytes (el resto es relleno) |
| Validación | las 39 funciones de `extabindex` coinciden con las del buscador |
| Tablas de `switch` | 203 (1 rechazada, en 0x801D136C) |
| Nombradas por firma del SDK | 1356, con la base de datos de firmas de Dolphin |
| Nombradas por `assert` | 15, con su archivo fuente (`cadFile.cpp`, `opeManager.cpp`…) |
| Bibliotecas del SDK | OS, EXI, SI, VI, GX, DVD, AI, AX, DSP, NAND, SC, PAD, WPAD, KPAD, THP, más el HOME Menu (HBM) |
| Bucle ocioso | `SelectThread+0x14C` (0x8013DE54), el mismo patrón que en Animal Parade |
| Escritores de la tubería de GX | 139 funciones, 1990 escrituras a 0xCC008000 |

Los nombres de los archivos fuente dan pistas de cómo está organizado el
juego: `cad*` es el motor (archivos, hilos, modelos, control), `ope*` son las
operaciones (`opeManager`, `opeObject_*` para cada enfermedad, `y_opeCut`,
`y_opeDirect`…), `scr*` los guiones de las escenas y `ttl*`/`sl*` la pantalla
de título y la de selección.

### El disco europeo

`RKDP01`, revisión 0, SHA-1 `7700acf2e73fbd5be907a0313ab70b8b204a2f79`. Su
`main.dol` es más grande (0x354560 contra 0x281920 bytes) y tiene 8220
funciones, con 2133 en `extabindex` contra 39 del USA: está compilado de otra
manera, no solo corrido de lugar. Pasar el mapa del USA al europeo será
emparejar funciones por su código, no sumar un desplazamiento.

---

## English

First map of `main.dol` from the USA disc (`RKDEEB`, revision 0, SHA-1
`e27a182b057741ce65c16d8789bcf6bdd3d9e52f`). Everything comes from
`config/RKDEEB/symbols.txt`, which is regenerated with:

```sh
python3 tools/extract_system_files.py "Trauma Center - Second Opinion (USA).rvz"
python3 tools/analyze.py
python3 tools/sdk_signatures.py --database path/to/Dolphin/Sys/totaldb.dsy --apply
```

### What was found

| | |
|---|---|
| Functions | 7802; code covers 0x21DA7C of 0x21F4E0 bytes (the rest is padding) |
| Validation | all 39 `extabindex` functions agree with the function finder |
| `switch` jump tables | 203 (1 rejected, at 0x801D136C) |
| Named by SDK signature | 1356, with Dolphin's signature database |
| Named by `assert` | 15, with their source file (`cadFile.cpp`, `opeManager.cpp`…) |
| SDK libraries | OS, EXI, SI, VI, GX, DVD, AI, AX, DSP, NAND, SC, PAD, WPAD, KPAD, THP, plus the HOME Menu (HBM) |
| Idle loop | `SelectThread+0x14C` (0x8013DE54), the same pattern as in Animal Parade |
| GX pipe writers | 139 functions, 1990 stores to 0xCC008000 |

The source file names hint at how the game is laid out: `cad*` is the engine
(files, threads, models, input), `ope*` are the operations (`opeManager`,
`opeObject_*` for each disease, `y_opeCut`, `y_opeDirect`…), `scr*` the scene
scripts and `ttl*`/`sl*` the title and select screens.

### The European disc

`RKDP01`, revision 0, SHA-1 `7700acf2e73fbd5be907a0313ab70b8b204a2f79`. Its
`main.dol` is bigger (0x354560 against 0x281920 bytes) and has 8220 functions,
with 2133 in `extabindex` against the USA's 39: it was built differently, not
just shifted. Carrying the USA map over to the European disc will mean pairing
functions by their code, not adding an offset.
