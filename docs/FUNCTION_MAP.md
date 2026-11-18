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

### Nombradas leyendo el código

Funciones del SDK que la base de firmas no reconoció, porque esta versión es
más vieja. `tools/port_addresses.py` encontró cinco por tener el mismo código
que en Animal Parade (`OSInitContext`, `__OSGetInterruptHandler`,
`IPCGetBufferHi`, `DSPCheckInit`, `DSPAssertTask`); estas diez se nombraron a
mano:

| Dirección | Nombre | Evidencia |
|---|---|---|
| 0x8015AC88 | `__AXOutInitDSP` | llena la tarea del DSP de AX (callbacks en +0x28…+0x34) y llama a `DSPAddTask` |
| 0x8015AC14 | `__AXDSPInitCallback` | pone en 1 la bandera que `__AXOutInitDSP` espera |
| 0x8015AC20 | `__AXDSPResumeCallback` | `__AXOutInitDSP` la guarda en +0x2C de la tarea |
| 0x8015AC74 | `__AXDSPRequestCallback` | ídem, en +0x30 |
| 0x8015AD6C | `__AXOutInit` | llama a `__AXOutInitDSP`, `AIInitDMA` y `AIStartDMA` |
| 0x8015EDD0 | `DSPAddTask` | `__DSP_insert_task` y luego `__DSP_boot_task`, justo después de `DSPCheckInit` |
| 0x8013F430 | `__OSDefaultPowerCallback` | un `blr` que `__OSInitSTM` guarda como callback de apagado |
| 0x801643F4 | `IPCGetBufferLo` | lee `IPCBufferLo`, junto a `IPCGetBufferHi` |
| 0x801643FC | `IPCSetBufferLo` | escribe `IPCBufferLo` |
| 0x8014C280 | `GXSetDrawDoneCallback` | cambia el callback con interrupciones apagadas, justo antes de `GXFinishInterruptHandler` |

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

### Named by reading the code

SDK functions the signature database did not recognize, because this version
is older. `tools/port_addresses.py` found five by having the same code as in
Animal Parade (`OSInitContext`, `__OSGetInterruptHandler`, `IPCGetBufferHi`,
`DSPCheckInit`, `DSPAssertTask`); these ten were named by hand:

| Address | Name | Evidence |
|---|---|---|
| 0x8015AC88 | `__AXOutInitDSP` | fills AX's DSP task (callbacks at +0x28…+0x34) and calls `DSPAddTask` |
| 0x8015AC14 | `__AXDSPInitCallback` | sets the flag `__AXOutInitDSP` waits on |
| 0x8015AC20 | `__AXDSPResumeCallback` | `__AXOutInitDSP` stores it at +0x2C of the task |
| 0x8015AC74 | `__AXDSPRequestCallback` | the same, at +0x30 |
| 0x8015AD6C | `__AXOutInit` | calls `__AXOutInitDSP`, `AIInitDMA` and `AIStartDMA` |
| 0x8015EDD0 | `DSPAddTask` | `__DSP_insert_task` then `__DSP_boot_task`, right after `DSPCheckInit` |
| 0x8013F430 | `__OSDefaultPowerCallback` | a `blr` that `__OSInitSTM` stores as the power callback |
| 0x801643F4 | `IPCGetBufferLo` | reads `IPCBufferLo`, next to `IPCGetBufferHi` |
| 0x801643FC | `IPCSetBufferLo` | writes `IPCBufferLo` |
| 0x8014C280 | `GXSetDrawDoneCallback` | swaps the callback with interrupts off, right before `GXFinishInterruptHandler` |

### The European disc

`RKDP01`, revision 0, SHA-1 `7700acf2e73fbd5be907a0313ab70b8b204a2f79`. Its
`main.dol` is bigger (0x354560 against 0x281920 bytes) and has 8220 functions,
with 2133 in `extabindex` against the USA's 39: it was built differently, not
just shifted. Carrying the USA map over to the European disc will mean pairing
functions by their code, not adding an offset.
