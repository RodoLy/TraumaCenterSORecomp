# Comodidades / Quality of life

Cambios que no alteran el juego, solo lo hacen más cómodo en PC. Cada uno vive en su propio parche
dentro de `patches/wiicompiled/`, viene apagado para que el juego arranque como el original, y se
enciende desde F10 o desde `UserData/Config.toml`.

Changes that leave the game itself alone and only make it more comfortable on a PC. Each one lives
in its own patch in `patches/wiicompiled/`, starts off so the game starts like the original, and can
be turned on in F10 or in `UserData/Config.toml`.

## Adelantar el texto / Hurrying text along

**Español.** Mantener presionada una tecla hace que todo el juego corra hasta cuatro veces más
rápido; sirve para pasar los diálogos largos. Viene apagado, como el juego original. Se enciende en
F10 > Controls > "Hold to fast-forward" (la tecla empieza como Tab y se puede cambiar, igual que un
botón del control).

**English.** Holding a key runs the whole game up to four times faster, which hurries long dialogue
along. It starts off, like the original game. Turn it on in F10 > Controls > "Hold to fast-forward"
(the key starts as Tab and can be changed, and so can a controller button).

```toml
[speed]
hold_to_fast_forward = true   # para encenderlo / to turn it on
```

## Pausa con la ventana en segundo plano / Pause in the background

**Español.** Si se enciende, cuando la ventana pierde el foco (Alt+Tab, otra ventana encima) el
juego se pausa igual que con su propia pausa, y sigue unos cuadros después de volver. Viene apagado,
como el original; se enciende en F10 > Controls con "Pause when the window is in the background" o
con `[controls] pause_when_unfocused = true`.

**English.** When on, the game pauses the same way its own pause does whenever the window loses
focus (Alt+Tab, another window on top), and carries on a few frames after the window comes back. It
starts off, like the original; turn it on in F10 > Controls with "Pause when the window is in the
background" or with `[controls] pause_when_unfocused = true`.

| Parche / Patch | Qué cambia / What it changes |
|---|---|
| `trauma-center-pause-in-background.patch` | `trauma_center_waits.cpp`: revisa el foco una vez por retrace y usa el contador de pausa del juego (0x803A6740) y su bandera 0x2 (0x803A73FC). / Checks the focus once per retrace and uses the game's pause counter (0x803A6740) and its flag 0x2 (0x803A73FC). |

## Saltar el arranque / Skipping the start-up

**Español.** Dos casillas en F10 > Mods > Trauma Center, apagadas al principio: "Skip the start-up
screens" hace que la advertencia de salud, el recordatorio de la correa y el logo pasen de inmediato;
"Skip the opening movie once seen" salta el video de apertura después de la primera vez que se vio.

**English.** Two checkboxes in F10 > Mods > Trauma Center, off at first: "Skip the start-up screens"
makes the health warning, the strap reminder and the logo go by at once; "Skip the opening movie
once seen" skips the opening movie after the first time it was seen.

| Parche / Patch | Qué cambia / What it changes |
|---|---|
| `trauma-center-skip-intro.patch` | Nuevo `trauma_center_comfort.cpp`. La tarea del título ("TTL DRAW PROC", 0x801215AC) guarda su paso en +0 y un contador en +0x18; en los pasos 2, 4 y 6 el contador se pone en su último cuadro. El paso 8 (el video) para el video cuando 0x80019238 responde 1. / New `trauma_center_comfort.cpp`. The title's task keeps its step at +0 and a counter at +0x18; in steps 2, 4 and 6 the counter is set to its last frame. Step 8 (the movie) stops the movie when 0x80019238 answers 1. |

```toml
[mods]
trauma_center_skip_start_screens = true   # para encenderlo / to turn it on
trauma_center_skip_seen_opening = true    # para encenderlo / to turn it on
trauma_center_opening_seen = true         # lo escribe el juego / written by the game
```

## Reintentar / Retrying

**Español.** El juego ya tiene "RETRY" en su menú de pausa (botón + o Enter), junto con "Episode
Select" y "PRACTICE", así que no hizo falta agregar nada.

**English.** The game already has "RETRY" in its pause menu (the + button or Enter), next to
"Episode Select" and "PRACTICE", so nothing had to be added.
