# Project plan / Plan del proyecto

[Español](#español) · [English](#english)

---

## Español

El mismo camino que el port de *Harvest Moon: Animal Parade*
([HarvestMoonAnimalParadeRecomp](https://github.com/RodoLy/HarvestMoonAnimalParadeRecomp)),
que también es de Wii. Las herramientas de análisis vienen de ahí.

**Meta: un port nativo, sin código de Dolphin**, sobre
[WiiCompiled](https://github.com/patchzyy/wiicompiled) y
[aurora](https://github.com/encounter/aurora). Mientras tanto, la versión que se
juega será la de ModernGekko (CPU recompilada; video, audio, disco y controles
del núcleo de Dolphin), como en Animal Parade.

Disco de referencia: *Trauma Center: Second Opinion* (USA), ID `RKDEEB`.

### Fase 0 – Mapa de funciones

- [ ] Extraer tu disco en `orig/RKDEEB/` y comprobarlo con
      `tools/check_disc.py`; anotar la revisión y el SHA-1 de `main.dol` que
      imprime.
- [ ] Generar `config/RKDEEB/symbols.txt` con `tools/analyze.py` y validar las
      funciones contra `extabindex`.
- [ ] Nombrar el SDK por firma (`tools/sdk_signatures.py`), con las bibliotecas
      de Wii (WPAD, KPAD, NAND, SC…).
- [ ] Encontrar el bucle ocioso (`tools/find_idle_loops.py`) y los escritores
      de la tubería de GX (`tools/find_gx_pipe_writers.py`).
- [ ] Escribir `docs/FUNCTION_MAP.md` con la evidencia de cada nombre.

### Fase 1 – Jugar con DolRecomp + ModernGekko

- [ ] Recompilar `main.dol` con DolRecomp en modo Wii.
- [ ] Llegar a la pantalla de título desde código recompilado.
- [ ] Puntero con el mouse y Nunchuk con teclado o control, como en Animal
      Parade.
- [ ] Paquete nativo para Windows x64 y Windows en ARM.

### Fase 2 – Runtime propio, sin Dolphin

- [ ] Manifiesto y mapa de funciones para el traductor de WiiCompiled.
- [ ] Las funciones nativas de WiiCompiled en las direcciones de este juego.
- [ ] Pantalla de título sin Dolphin, comparada con la de ModernGekko.
- [ ] Hito 1.0: jugable de principio a fin sin código de Dolphin.

### Fase 3 – Mejoras

- Resolución alta y pantalla ancha. El juego original no tiene 16:9, así que
  será un mod: las cirugías en 3D ven más a los lados y las escenas en 2D
  (retratos, textos, menús) se quedan en 4:3 al centro.
- El puntero tiene que caer exactamente donde apunta el mouse también en
  pantalla ancha: en este juego un corte fuera de lugar es un error del jugador.
- Gestos del Wii Remote y del Nunchuk mapeados a teclas, botones o el mouse.
- Que dibujar la estrella del Healing Touch se sienta bien con el mouse.
- Mods con la ABI de ModernGekko (`RECOMP_PATCH`, `RECOMP_HOOK`).

### Por defecto

Por defecto todo viene como en el juego original. Las mejoras se eligen en el
launcher o en el menú del juego.

---

## English

The same path as the *Harvest Moon: Animal Parade* port
([HarvestMoonAnimalParadeRecomp](https://github.com/RodoLy/HarvestMoonAnimalParadeRecomp)),
which is also a Wii game. The analysis tools come from there.

**Goal: a native port, with no Dolphin code**, on
[WiiCompiled](https://github.com/patchzyy/wiicompiled) and
[aurora](https://github.com/encounter/aurora). Meanwhile, the version that is
played will be ModernGekko's (recompiled CPU; video, audio, disc and input from
the Dolphin core), as in Animal Parade.

Reference disc: *Trauma Center: Second Opinion* (USA), ID `RKDEEB`.

### Phase 0 – Function map

- [ ] Extract your disc into `orig/RKDEEB/` and check it with
      `tools/check_disc.py`; record the revision and the `main.dol` SHA-1 it
      prints.
- [ ] Generate `config/RKDEEB/symbols.txt` with `tools/analyze.py` and validate
      the functions against `extabindex`.
- [ ] Name the SDK by signature (`tools/sdk_signatures.py`), with the Wii
      libraries (WPAD, KPAD, NAND, SC…).
- [ ] Find the idle loop (`tools/find_idle_loops.py`) and the GX pipe writers
      (`tools/find_gx_pipe_writers.py`).
- [ ] Write `docs/FUNCTION_MAP.md` with the evidence for every name.

### Phase 1 – Play with DolRecomp + ModernGekko

- [ ] Recompile `main.dol` with DolRecomp in Wii mode.
- [ ] Reach the title screen from recompiled code.
- [ ] Mouse as the pointer and the Nunchuk on keyboard or gamepad, as in
      Animal Parade.
- [ ] Native package for Windows x64 and Windows on ARM.

### Phase 2 – Our own runtime, without Dolphin

- [ ] Manifest and function map for WiiCompiled's translator.
- [ ] WiiCompiled's native functions at this game's addresses.
- [ ] Title screen without Dolphin, compared with ModernGekko's.
- [ ] Milestone 1.0: playable from start to finish with no Dolphin code.

### Phase 3 – Improvements

- High resolution and widescreen. The original game has no 16:9 mode, so it
  will be a mod: the 3D surgeries see more at the sides, and the 2D scenes
  (portraits, text, menus) stay 4:3 in the middle.
- The pointer has to land exactly where the mouse points in widescreen too: in
  this game a cut in the wrong place is the player's mistake.
- Wii Remote and Nunchuk gestures mapped to keys, buttons or the mouse.
- Drawing the Healing Touch star should feel right with the mouse.
- Mods with ModernGekko's ABI (`RECOMP_PATCH`, `RECOMP_HOOK`).

### By default

Everything starts as in the original game. Improvements are chosen in the
launcher or in the in-game menu.
