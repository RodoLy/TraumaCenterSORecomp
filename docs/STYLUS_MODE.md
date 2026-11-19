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

| Modo | Para quién | Controles | Textos |
|---|---|---|---|
| **Wii Remote** | Quien juega con un Wii Remote real o con un control | Los del Wii | Los originales |
| **Stylus** | Quien juega solo con mouse (o pantalla táctil) | Todo con puntero y clic | Cambiados para el mouse |

### Cada acción del Wii y su equivalente en modo stylus

| Acción en el Wii | Cómo se hace en el Wii | Modo stylus | Estado |
|---|---|---|---|
| Elegir herramienta | Stick del Nunchuk hacia una de las 8 direcciones | Clic sobre su hexágono del menú (como tocar el ícono en DS) | Hecho |
| Bisturí, sutura, gel, drenaje, láser, jeringa (aplicar) | Apuntar y apretar o mantener A | Clic o clic sostenido y arrastrar | Hecho (es el A de siempre) |
| Pinzas (agarrar) | Apretar A y B a la vez, como pellizcando | Mantener el clic: a la décima de segundo se suma B | Hecho, por probar |
| Healing Touch | Mantener Z y B y dibujar una estrella | Mantener el clic derecho y dibujar la estrella | Por hacer |
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

Los diálogos de las operaciones están en `files/operation/msg_ope/opeXXX.bm2` (y empaquetados en
`msg_ope.pak`), los de las escenas en `msg_evt` y los de las conferencias de cada caso en `msg_cnf`.
Usan el formato de mensajes de Atlus «MSG2»: cabecera `MSG2`, una tabla de mensajes y el texto en ASCII
con códigos de control en medio (pausas, colores, cara del personaje).

El mod **no trae el guion del juego**. Trae solo una tabla con el archivo, el número de mensaje y una
frase nueva escrita por nosotros. Al cargar esos archivos de tu disco, WiiCompiled reemplaza esos
mensajes al vuelo, conservando los códigos de control del original, y solo en modo stylus.

Pasos:

1. Leer y escribir el formato MSG2 (herramienta en `tools/`, con pruebas).
2. Listar los mensajes que hablan de controles: stick, A, B, Z, «Wii Remote», «Nunchuk», empujar,
   girar. La búsqueda se hace sobre el disco del usuario y la lista guarda solo números de mensaje.
3. Escribir las frases nuevas (en inglés, como el juego), cuidando que quepan en el cuadro de texto.
4. Reemplazarlas al cargar el archivo, en el lector de DVD de WiiCompiled.
5. Revisar cada operación del tutorial en el juego.

Más adelante, la misma tabla sirve para la traducción al español del disco europeo.

---

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

| Mode | For whom | Controls | Text |
|---|---|---|---|
| **Wii Remote** | Players with a real Wii Remote or a controller | The Wii's | The original |
| **Stylus** | Players with a mouse only (or a touch screen) | Pointer and click | Rewritten for the mouse |

### Every Wii action and its stylus-mode equivalent

| Action on the Wii | How it is done on the Wii | Stylus mode | Status |
|---|---|---|---|
| Pick a tool | Nunchuk stick toward one of 8 directions | Click its hexagon in the menu (like tapping the DS icon) | Done |
| Scalpel, sutures, gel, drain, laser, syringe (apply) | Point and press or hold A | Click, or hold the click and drag | Done (plain A) |
| Forceps (grab) | Press A and B together, a pinch | Hold the click: after a tenth of a second B joins A | Done, to be tested |
| Healing Touch | Hold Z and B and draw a star | Hold the right button and draw the star | To do |
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

The operations' dialogue is in `files/operation/msg_ope/opeXXX.bm2` (and packed in `msg_ope.pak`), the
story scenes' in `msg_evt` and each case's briefing in `msg_cnf`. They use Atlus's "MSG2" message
format: a `MSG2` header, a message table and ASCII text with control codes in between (pauses,
colours, the character's face).

The mod **does not ship the game's script**. It only ships a table with the file, the message number
and a new line we wrote ourselves. When those files load from your disc, WiiCompiled replaces those
messages on the fly, keeping the original's control codes, and only in stylus mode.

Steps:

1. Read and write the MSG2 format (a tool in `tools/`, with tests).
2. List the messages that talk about controls: stick, A, B, Z, "Wii Remote", "Nunchuk", push, turn.
   The search runs on the user's disc and the list keeps only message numbers.
3. Write the new lines (in English, like the game), making sure they fit the text box.
4. Replace them when the file loads, in WiiCompiled's DVD reader.
5. Check every tutorial operation in the game.

Later on, the same table can carry the Spanish translation from the European disc.
