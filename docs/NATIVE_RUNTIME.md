# Native runtime / Runtime nativo

[Español](#español) · [English](#english)

---

## Español

El camino para que el juego corra nativo en Windows (x64 y ARM64), sin
Dolphin: el mismo que tomó el
[port de Animal Parade](https://github.com/RodoLy/HarvestMoonAnimalParadeRecomp/blob/main/docs/NATIVE_RUNTIME.md),
con [WiiCompiled](https://github.com/patchzyy/wiicompiled). Su traductor
convierte el código del juego en C++ y su runtime reemplaza partes del SDK de
Nintendo (sistema, gráficos, video, disco, audio) por código nativo.

Ese código nativo busca funciones y variables del SDK en las direcciones de
*Mario Kart Wii*. Para cada una, este juego necesita la suya: eso son las
tablas `wiicompiled/RKDEEB-*-addresses.txt`.

### Cómo se llenaron

`tools/port_addresses.py` toma las tablas del port de Animal Parade, que ya
tienen cada dirección con su evidencia, y busca lo mismo aquí:

1. una función, por su nombre; si la base de firmas no la nombró, por su
   código (así se nombraron cinco funciones más en `symbols.txt`);
2. una variable, por el orden en que la alcanza la función de la evidencia;
3. si esa función no existe aquí o se compiló distinto, por cualquier otra
   función que alcance la variable, y todas tienen que coincidir.

`tests/test_wiicompiled_addresses.py` vuelve a comprobar cada fila contra
`main.dol` (con `TC_SO_DOL` apuntando a tu `orig/RKDEEB/sys/main.dol`).

### Cómo van

| Tabla | Filas listas |
|---|---|
| startup | 5 de 5 |
| os | 30 de 31 |
| sc | 2 de 3 |
| storage (DVD, NAND, IPC) | 23 de 27 |
| gx | 28 de 37 |
| vi | 9 de 14 |
| audio | 11 de 26 |
| **Total** | **108 de 143** |

### Lo que falta, y por qué

*Second Opinion* salió con el Wii en 2006 y trae un SDK más viejo que Animal
Parade o Mario Kart Wii (2008). Las 35 filas que faltan están justo donde el
SDK cambió:

- **Audio (15).** La versión de AX es anterior: no tiene las funciones de las
  que salía la evidencia (`__AXOutInitDSP`, los callbacks del DSP, la reverb
  `AXFXReverbStd`; este juego usa `AXFXReverbHi`). Además, el audio nativo de
  WiiCompiled lee los bloques de parámetros de cada voz con la forma de 2008;
  hay que revisar que este AX tenga la misma forma. **Es el riesgo más
  grande.**
- **Listas de comandos de GX (8).** El juego no enlaza `GXBeginDisplayList`
  ni `GXEndDisplayList`; si de verdad nunca arma listas, esas filas quedan en
  "-".
- **VI (5)**, **DVD y NAND (4)**, `IPCSetBufferLo`, `GXSetDrawDoneCallback`,
  `__OSDefaultPowerCallback` y la tabla de regiones de SC: código que cambió
  entre versiones del SDK. Hay que encontrarlos leyendo el código.

---

## English

The path to running the game natively on Windows (x64 and ARM64), without
Dolphin: the one the
[Animal Parade port](https://github.com/RodoLy/HarvestMoonAnimalParadeRecomp/blob/main/docs/NATIVE_RUNTIME.md)
took, with [WiiCompiled](https://github.com/patchzyy/wiicompiled). Its
translator turns the game's code into C++, and its runtime replaces parts of
Nintendo's SDK (system, graphics, video, disc, audio) with native code.

That native code looks for SDK functions and variables at *Mario Kart Wii*'s
addresses. This game needs its own address for each one: those are the
`wiicompiled/RKDEEB-*-addresses.txt` tables.

### How they were filled in

`tools/port_addresses.py` takes the Animal Parade port's tables, which already
hold each address with its evidence, and looks for the same thing here:

1. a function, by its name; when the signature database did not name it, by
   its code (that is how five more functions got their names in
   `symbols.txt`);
2. a variable, by the order in which the evidence function reaches it;
3. when that function is missing here or was built differently, through every
   other function that reaches the variable, which must all agree.

`tests/test_wiicompiled_addresses.py` checks every row again against
`main.dol` (with `TC_SO_DOL` pointing at your `orig/RKDEEB/sys/main.dol`).

### Where they stand

| Table | Rows done |
|---|---|
| startup | 5 of 5 |
| os | 30 of 31 |
| sc | 2 of 3 |
| storage (DVD, NAND, IPC) | 23 of 27 |
| gx | 28 of 37 |
| vi | 9 of 14 |
| audio | 11 of 26 |
| **Total** | **108 of 143** |

### What is left, and why

*Second Opinion* launched with the Wii in 2006 and carries an older SDK than
Animal Parade or Mario Kart Wii (2008). The 35 rows left are exactly where the
SDK changed:

- **Audio (15).** Its AX is older: it lacks the functions the evidence came
  from (`__AXOutInitDSP`, the DSP callbacks, the `AXFXReverbStd` reverb; this
  game uses `AXFXReverbHi`). On top of that, WiiCompiled's native audio reads
  each voice's parameter block in the 2008 shape; this AX has to be checked
  for the same shape. **This is the biggest risk.**
- **GX display lists (8).** The game does not link `GXBeginDisplayList` or
  `GXEndDisplayList`; if it really never builds lists, those rows become "-".
- **VI (5)**, **DVD and NAND (4)**, `IPCSetBufferLo`, `GXSetDrawDoneCallback`,
  `__OSDefaultPowerCallback` and SC's region table: code that changed between
  SDK versions. They have to be found by reading the code.
