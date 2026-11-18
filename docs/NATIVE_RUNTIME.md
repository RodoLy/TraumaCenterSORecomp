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

### Cómo quedaron

Las 143 filas están completas y comprobadas. La herramienta pasó 108; las
otras 35 se encontraron leyendo el código, porque *Second Opinion* salió con
el Wii en 2006 y trae un SDK más viejo que Animal Parade o Mario Kart Wii
(2008). Las tablas ya no se regeneran con la herramienta: se mantienen a mano.

Lo que se aprendió en el camino:

- **El audio sí encaja.** El microcódigo de AX de este juego tiene el checksum
  `0xFA450138`, el AX viejo de los primeros juegos de Wii, y el mezclador de
  WiiCompiled ya lo conoce (es la variante que Dolphin llama "old AXWii"). Lo
  que cambia es la DRAM de la tarea: 0x2000 bytes en la dirección 0 del DSP,
  donde Mario Kart Wii usa 0x40 bytes en 0xCD2. WiiCompiled escribe los
  valores de Mario Kart Wii; hay que revisar al probarlo si eso importa.
- **La reverb estándar** (`AXFXReverbStd`) no existe aquí; el juego usa
  `AXFXReverbHi`, que corre traducida. Esas filas quedan en "-".
- **El juego nunca arma listas de comandos de GX** (no enlaza
  `GXBeginDisplayList`), así que esas variables tampoco existen.
- **VI** guarda sus variables en otro orden: cada una se encontró por lo que
  hace el código con ella.

### La capa del juego

- `wiicompiled/RKDEEB.yml`: el manifiesto para el traductor.
- `wiicompiled/RKDEEB-MAP.txt`: las 7838 funciones, de `tools/export_wiicompiled_map.py`.
- `tools/export_wiicompiled_layer.py` coloca 260 de las 582 funciones nativas
  de WiiCompiled en las direcciones de este juego (Animal Parade: 302). Las que
  faltan son funciones del SDK que este juego no tiene o que todavía no tienen
  nombre; esas corren traducidas.
- `tools/name_from_reference_game.py` nombró 83 funciones del SDK copiando los
  nombres de Animal Parade donde el código es idéntico.
- El IOS es el 9, como dice el TMD del disco; el `OSInit` de este juego no se
  detiene si no coincide.

### Lo que sigue

Correr el workflow del paquete de Windows ARM64 y probarlo: traducir, compilar
y llegar a la pantalla de título.

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

### How they ended up

All 143 rows are filled in and checked. The tool carried over 108; the other
35 were found by reading the code, because *Second Opinion* launched with the
Wii in 2006 and carries an older SDK than Animal Parade or Mario Kart Wii
(2008). The tables are no longer regenerated with the tool: they are kept by
hand.

What was learned on the way:

- **The audio does fit.** This game's AX microcode has the checksum
  `0xFA450138`, the old AX of the first Wii games, and WiiCompiled's mixer
  already knows it (the variant Dolphin calls "old AXWii"). What differs is
  the task's DRAM: 0x2000 bytes at DSP address 0, where Mario Kart Wii uses
  0x40 bytes at 0xCD2. WiiCompiled writes Mario Kart Wii's values; whether
  that matters is to be seen when testing.
- **The standard reverb** (`AXFXReverbStd`) is not here; the game uses
  `AXFXReverbHi`, which runs translated. Those rows are "-".
- **The game never builds GX display lists** (it does not link
  `GXBeginDisplayList`), so those variables do not exist either.
- **VI** keeps its variables in another order: each was found by what the
  code does with it.

### The game layer

- `wiicompiled/RKDEEB.yml`: the manifest for the translator.
- `wiicompiled/RKDEEB-MAP.txt`: the 7838 functions, from `tools/export_wiicompiled_map.py`.
- `tools/export_wiicompiled_layer.py` places 260 of WiiCompiled's 582 natives
  at this game's addresses (Animal Parade: 302). The rest are SDK functions this
  game does not have or that are not named yet; those run translated.
- `tools/name_from_reference_game.py` named 83 SDK functions by copying Animal
  Parade's names where the code is identical.
- The IOS is 9, as the disc's TMD says; this game's `OSInit` does not stop when
  it differs.

### What comes next

Run the Windows ARM64 package workflow and test it: translate, compile and
reach the title screen.
