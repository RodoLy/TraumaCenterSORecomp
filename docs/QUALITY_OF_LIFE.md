# Comodidades / Quality of life

Cambios que no alteran el juego, solo lo hacen más cómodo en PC. Cada uno vive en su propio parche
dentro de `patches/wiicompiled/` y se puede apagar desde F10 o desde `UserData/Config.toml`.

Changes that leave the game itself alone and only make it more comfortable on a PC. Each one lives
in its own patch in `patches/wiicompiled/` and can be turned off in F10 or in `UserData/Config.toml`.

## Adelantar el texto / Hurrying text along

**Español.** Mantener presionada la tecla Tab hace que todo el juego corra hasta cuatro veces más
rápido; sirve para pasar los diálogos largos. Ahora viene encendido. La tecla (y un botón del
control) se cambian en F10 > Controls > "Hold to fast-forward".

**English.** Holding Tab runs the whole game up to four times faster, which hurries long dialogue
along. It is now on by default. The key (and a controller button) can be changed in F10 > Controls >
"Hold to fast-forward".

| Parche / Patch | Qué cambia / What it changes |
|---|---|
| `trauma-center-fast-forward-on.patch` | `vi.cpp` y `settings_overlay.cpp`: el valor por defecto pasa de apagado a encendido. / The default goes from off to on. |

```toml
[speed]
hold_to_fast_forward = false   # para apagarlo / to turn it off
```

## Pausa con la ventana en segundo plano / Pause in the background

**Español.** Si la ventana pierde el foco (Alt+Tab, otra ventana encima), el juego se pausa igual
que con su propia pausa, y sigue unos cuadros después de volver. Se apaga en F10 con "Pause when the
window is in the background" o con `[controls] pause_when_unfocused = false`.

**English.** When the window loses focus (Alt+Tab, another window on top), the game pauses the same
way its own pause does, and carries on a few frames after the window comes back. Turn it off in F10
with "Pause when the window is in the background" or with `[controls] pause_when_unfocused = false`.

| Parche / Patch | Qué cambia / What it changes |
|---|---|
| `trauma-center-pause-in-background.patch` | `trauma_center_waits.cpp`: revisa el foco una vez por retrace y usa el contador de pausa del juego (0x803A6740) y su bandera 0x2 (0x803A73FC). / Checks the focus once per retrace and uses the game's pause counter (0x803A6740) and its flag 0x2 (0x803A73FC). |

## Saltar el arranque / Skipping the start-up

**Español.** La advertencia de salud, el recordatorio de la correa y el logo pasan de inmediato. El
video de apertura se ve una vez y después se salta. Ambas cosas se apagan en F10 > Mods > Trauma
Center ("Skip the start-up screens", "Skip the opening movie once seen").

**English.** The health warning, the strap reminder and the logo go by at once. The opening movie
plays once and is skipped from then on. Both can be turned off in F10 > Mods > Trauma Center ("Skip
the start-up screens", "Skip the opening movie once seen").

| Parche / Patch | Qué cambia / What it changes |
|---|---|
| `trauma-center-skip-intro.patch` | Nuevo `trauma_center_comfort.cpp`. La tarea del título ("TTL DRAW PROC", 0x801215AC) guarda su paso en +0 y un contador en +0x18; en los pasos 2, 4 y 6 el contador se pone en su último cuadro. El paso 8 (el video) para el video cuando 0x80019238 responde 1. / New `trauma_center_comfort.cpp`. The title's task keeps its step at +0 and a counter at +0x18; in steps 2, 4 and 6 the counter is set to its last frame. Step 8 (the movie) stops the movie when 0x80019238 answers 1. |

```toml
[mods]
trauma_center_skip_start_screens = true
trauma_center_skip_seen_opening = true
trauma_center_opening_seen = true    # lo escribe el juego / written by the game
```

## Reintentar / Retrying

**Español.** El juego ya tiene "RETRY" en su menú de pausa (botón + o Enter), junto con "Episode
Select" y "PRACTICE", así que no hizo falta agregar nada.

**English.** The game already has "RETRY" in its pause menu (the + button or Enter), next to
"Episode Select" and "PRACTICE", so nothing had to be added.

## Selección de capítulo / Chapter select

**Español.** En la pantalla de título, F10 > Mods > Chapter select > "Start at" elige un capítulo
(1 a 6) o "Every episode". Después, New Game o cargar una partida: el Episode Select del juego ofrece
todos los episodios hasta ese capítulo. Mientras esté activo **no se puede guardar** (el juego dice
que falló al guardar) y tus datos no cambian. No se guarda en Config.toml: el juego siempre arranca
normal.

**English.** On the title screen, F10 > Mods > Chapter select > "Start at" picks a chapter (1 to 6)
or "Every episode". Then start a New Game or load a file: the game's Episode Select offers every
episode up to that chapter. While it is on, **saving is off** (the game says the save failed) and
your data does not change. It is not kept in Config.toml: the game always starts normal.

| Parche / Patch | Qué cambia / What it changes |
|---|---|
| `trauma-center-chapter-select.patch` | Nuevo `trauma_center_chapter_select.cpp`. 0x80015CFC prueba un bit del progreso (`*(0x803A7488)` + 0x40; el bit de un episodio es 0x50 + su número); con un capítulo elegido responde "alcanzado" para los episodios anteriores. 0x8001CEBC empieza toda escritura a la memoria del Wii; con un capítulo elegido no escribe y deja el error -1. / New `trauma_center_chapter_select.cpp`. 0x80015CFC tests a progress bit (`*(0x803A7488)` + 0x40; an episode's bit is 0x50 plus its number); with a chapter chosen it answers "reached" for the episodes before it. 0x8001CEBC starts every write to the Wii's memory; with a chapter chosen it writes nothing and leaves the error -1. |
