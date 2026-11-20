# Stylus mode / Modo stylus

[Español](#español) · [English](#english)

---

## Español

### Qué es

Trauma Center: Second Opinion es la versión para Wii de *Trauma Center: Under the Knife* de DS. En DS
todo se hacía con el stylus: tocar un ícono para cambiar de herramienta, arrastrar para cortar o
suturar, tocar para el láser y dibujar una estrella para el Healing Touch. En Wii, el stick del Nunchuk
elige la herramienta en un menú circular de ocho direcciones y el Wii Remote la usa, con algunas
acciones nuevas que piden mover los controles.

El **modo stylus** devuelve el juego a la forma del DS en una PC: **todo se hace con el puntero del
mouse y el clic**, sin stick y sin gestos. Los textos que explican los controles del Wii se cambian por
otros que explican el mouse.

El port tendrá dos modos, elegibles en F10 y en `UserData\Config.toml`:

| Modo (F10 → Controller settings → Controls, o `[controls] mode` en Config.toml) | Controles |
|---|---|
| **Solo mouse** (`mouse`) | Como el stylus de DS: clic en una herramienta para elegirla, clic sostenido para agarrar, clic derecho sostenido para el Healing Touch |
| **Mouse y teclado** (`mouse_keys`) | El mouse apunta y hace clic; las teclas 1 a 8 eligen herramientas (en el sentido del reloj desde la de arriba), Espacio agarra, Shift izquierdo es B y Q es Z (las dos juntas: el Healing Touch) |
| **Mouse y control** (`mouse_controller`) | El mouse apunta y hace clic; el stick del control elige herramientas y sus botones hacen lo demás, como el Nunchuk |

En los tres, lo del mouse funciona siempre; el modo agrega las teclas y decide qué instrucciones
muestra el juego (cuando estén los textos).

### Cada acción del Wii y su equivalente en modo stylus

| Acción en el Wii | Cómo se hace en el Wii | Modo stylus | Estado |
|---|---|---|---|
| Elegir herramienta | Stick del Nunchuk hacia una de las 8 direcciones | Clic sobre su hexágono del menú (como tocar el ícono en DS) | Hecho |
| Bisturí, sutura, gel, drenaje, láser, jeringa (aplicar) | Apuntar y apretar o mantener A | Clic o clic sostenido y arrastrar | Hecho (es el A de siempre) |
| Pinzas (agarrar) | Apretar A y B a la vez, como pellizcando | Mantener el clic: a la décima de segundo se suma B | Hecho, por probar |
| Healing Touch | Mantener Z y B y dibujar una estrella | Mantener el clic derecho y dibujar la estrella (a los 0.3 s se suma Z) | Hecho, por probar |
| Desfibrilador | Empujar el Wii Remote y el Nunchuk hacia la pantalla; luego B y Z cuando el medidor llega al nivel | Clic sobre el paciente coloca las paletas (el mod simula el empuje); otro clic descarga (B + Z) | Por hacer |
| Girar fragmentos de hueso | Girar el Wii Remote en la mano | Rueda del mouse mientras se sostiene el fragmento | Por hacer |
| Empujar o jalar hacia la pantalla | Acercar o alejar el Wii Remote | Rueda del mouse | Por hacer, falta ver qué operaciones lo piden |
| Pausa | Botón + | Botón lateral del mouse, o Esc | Hecho (botón lateral) |
| Menús, diálogos | Apuntar y A | Clic | Hecho |

Las acciones «por hacer» se confirman jugando: hay que ver en qué operación aparece cada una y qué lee
el juego exactamente (botones, acelerómetro o la cámara del Wii Remote) antes de simularla.

### Cómo se simula cada cosa

Todo vive en el Wii Remote virtual de WiiCompiled (`emulated_remote_host.cpp`), que ya traduce el mouse
a un Wii Remote con Nunchuk. El modo stylus solo cambia **qué** le manda al juego:

- **Herramientas:** el menú circular está siempre en el mismo lugar (centro en (100, 387) de la imagen
  de 640×480). Un clic sobre un hexágono empuja el stick hacia él en lugar de apretar A.
- **Pellizco:** un clic sostenido suma B a A. Un clic rápido sigue siendo solo A, para no afectar menús.
- **Gestos de movimiento:** el Wii Remote virtual envía acelerómetro fijo («en reposo»). Para el
  desfibrilador se envía, durante unos cuadros, el pico de aceleración hacia adelante en los dos
  controles. Para girar se rota el par de puntos de la barra de sensores, que es como el juego mide el
  giro, o el acelerómetro, según lo que lea esta versión del juego.
- **Puntero exacto:** el puntero se calcula sobre la imagen 4:3 y no sobre toda la ventana. La
  corrección fina sale de comparar en el registro la posición que se manda con la que calcula el juego.

### Los textos

Las líneas de los tutoriales que nombran botones del Wii Remote se cambian según el modo elegido,
cuando el juego las lee del disco (`trauma-center-control-texts.patch`,
`runtime/src/hle/game_mods/trauma_center_control_texts.cpp`). Son 14 líneas:

| Dónde | Qué dice el juego | Solo mouse | Mouse y teclado | Mouse y control |
|---|---|---|---|---|
| Pinzas (operación 1-1) | A y B | mantener el clic izquierdo | Espacio o el clic izquierdo | sin cambio |
| Ultrasonido (1-2) | B | clic derecho | Shift izquierdo | sin cambio |
| Lupa (1-5) | A | clic | clic | sin cambio |
| Desfibrilador (1-8) | B y Z juntos | mantener el clic derecho | Shift izquierdo y Q | B y LT (L2) |
| Healing Touch (2-3) | Z, luego B | mantener el clic derecho | Q, luego Shift izquierdo | LT (L2), luego B |
| Menú de episodios | Z o C para la dificultad | botón de en medio o lateral | Q o E | LT o RT (L2/R2) |

Cada línea nueva es igual o más corta que la original (se rellena con espacios), así que los archivos
no cambian de tamaño. El texto del juego no está en el repositorio: la tabla guarda la posición, el
largo y un hash de cada línea, y antes de cambiarla se revisa ese hash contra el disco.
`tools/control_texts.py` vuelve a generar la tabla desde el disco. Los textos se leen al iniciar el
juego, así que un cambio de modo se ve en ellos después de reiniciar.

Falta: la imagen de ayuda de controles de la pausa (`pause/i_allcon_help01.tpx`) es una textura, no
texto.

## English

### What it is

Trauma Center: Second Opinion is the Wii version of the DS game *Trauma Center: Under the Knife*. On
the DS everything was done with the stylus: tap an icon to switch tools, drag to cut or stitch, tap for
the laser and draw a star for the Healing Touch. On the Wii, the Nunchuk's stick picks the tool from an
eight-way radial menu and the Wii Remote wields it, with a few new actions that ask you to move the
controllers.

**Stylus mode** brings the game back to the DS's way on a PC: **everything with the mouse pointer and
the click**, with no stick and no gestures. The lines that explain the Wii's controls are replaced
with ones that explain the mouse.

The port will have two modes, chosen in F10 and in `UserData\Config.toml`:

| Mode (F10 → Controller settings → Controls, or `[controls] mode` in Config.toml) | Controls |
|---|---|
| **Mouse only** (`mouse`) | Like the DS stylus: click a tool to pick it, hold the click to grab, hold the right button for the Healing Touch |
| **Mouse and keyboard** (`mouse_keys`) | The mouse points and clicks; keys 1 to 8 pick tools (clockwise from the top one), Space grabs, Left Shift is B and Q is Z (both held: the Healing Touch) |
| **Mouse and controller** (`mouse_controller`) | The mouse points and clicks; the controller's stick picks tools and its buttons do the rest, like the Nunchuk |

In all three, the mouse always works; the mode adds the keys and decides which instructions the game
shows (once the texts are in).

### Every Wii action and its stylus-mode equivalent

| Action on the Wii | How it is done on the Wii | Stylus mode | Status |
|---|---|---|---|
| Pick a tool | Nunchuk stick toward one of 8 directions | Click its hexagon in the menu (like tapping the DS icon) | Done |
| Scalpel, sutures, gel, drain, laser, syringe (apply) | Point and press or hold A | Click, or hold the click and drag | Done (plain A) |
| Forceps (grab) | Press A and B together, a pinch | Hold the click: after a tenth of a second B joins A | Done, to be tested |
| Healing Touch | Hold Z and B and draw a star | Hold the right button and draw the star (after 0.3 s Z joins B) | Done, to be tested |
| Defibrillator | Push the Wii Remote and Nunchuk toward the screen, then B and Z when the gauge reaches the mark | A click on the patient places the paddles (the mod fakes the push); another click shocks (B + Z) | To do |
| Turn bone fragments | Turn the Wii Remote in the hand | Mouse wheel while holding the fragment | To do |
| Push or pull toward the screen | Move the Wii Remote closer or farther | Mouse wheel | To do, still to see which operations ask for it |
| Pause | + button | Mouse side button, or Esc | Done (side button) |
| Menus, dialogue | Point and A | Click | Done |

The "to do" actions are confirmed by playing: first see where each one appears and what exactly the
game reads (buttons, accelerometer or the Wii Remote's camera), then fake that.

### How each one is faked

Everything lives in WiiCompiled's emulated Wii Remote (`emulated_remote_host.cpp`), which already turns
the mouse into a Wii Remote with a Nunchuk. Stylus mode only changes **what** it sends the game:

- **Tools:** the radial menu always sits in the same place (center at (100, 387) of the 640×480
  picture). A click on a hexagon pushes the stick toward it instead of pressing A.
- **Pinch:** a held click adds B to A. A quick click is still A alone, so menus are not affected.
- **Motion gestures:** the emulated remote sends a fixed accelerometer ("at rest"). For the
  defibrillator it sends, for a few frames, the forward acceleration spike on both controllers. For
  turning it rotates the sensor bar's two dots, which is how the game measures roll, or the
  accelerometer, whichever this version of the game reads.
- **Exact pointer:** the pointer is computed over the 4:3 picture, not the whole window. The fine
  correction comes from comparing, in the log, the position sent with the one the game works out.

### The text

The tutorial lines that name the Wii Remote's buttons are swapped for the chosen mode as the game
reads them from the disc (`trauma-center-control-texts.patch`,
`runtime/src/hle/game_mods/trauma_center_control_texts.cpp`). There are 14 lines:

| Where | What the game says | Mouse only | Mouse and keyboard | Mouse and controller |
|---|---|---|---|---|
| Forceps (operation 1-1) | A and B | hold the left button | Space or the left button | unchanged |
| Ultrasound (1-2) | B | right button | Left Shift | unchanged |
| Magnifier (1-5) | A | click | click | unchanged |
| Defibrillator (1-8) | B and Z together | hold the right button | Left Shift and Q | B and LT (L2) |
| Healing Touch (2-3) | Z, then B | hold the right button | Q, then Left Shift | LT (L2), then B |
| Episode menu | Z or C for the difficulty | middle or side button | Q or E | LT or RT (L2/R2) |

Every new line is as long as the original or shorter (padded with spaces), so the files keep their
size. The game's text is not in the repository: the table keeps each line's position, length and a
hash, and the hash is checked against the disc before the line is changed. `tools/control_texts.py`
regenerates the table from the disc. The texts are read when the game starts, so a new mode shows in
them after a restart.

Still to do: the pause menu's controls help (`pause/i_allcon_help01.tpx`) is a picture, not text.
