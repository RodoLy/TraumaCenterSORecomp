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
