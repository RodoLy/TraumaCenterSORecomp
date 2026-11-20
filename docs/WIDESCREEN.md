# Pantalla ancha / Widescreen

## Español

Trauma Center: Second Opinion está hecho para 4:3. Con la opción de pantalla ancha (F10 → Graphics →
Wide picture), el port decide cuadro por cuadro qué hacer con cada dibujo.

### Cuadros con modelos 3D (las operaciones)

- **La cámara 3D se abre.** El juego conserva su cámara 4:3 para sus cálculos (dónde van la herida,
  las suturas y las líneas guía), y solo la copia que va a la tarjeta de video se hace ancha. Así el
  cuerpo y las marcas coinciden, y a los lados se ve más del quirófano.
  Parche: `trauma-center-wide-camera.patch`.
- **Lo que cubre toda la imagen** (el fondo borroso, los velos sobre la escena) se amplía parejo hasta
  llenar la pantalla: no se deforma, solo pierde un poco arriba y abajo.
  Parche: `aurora-wide-picture-whole-pictures.patch`.
- **Las franjas que cruzan la imagen** (el panel oscuro y la línea de abajo) se estiran a lo ancho.
  Parche: `aurora-wide-picture-bands.patch`.
- **Las franjas hechas de varios pedazos** (las rayas de arriba: extremo izquierdo, centro, extremo
  derecho): cada extremo se jala hasta la orilla de la pantalla y su otro lado se queda pegado al
  centro. Parche: `aurora-wide-picture-band-ends.patch`.
- **Todo lo demás** (números, hexágono de herramientas, enfermera, texto) se queda en 4:3, en su lugar.

### Cuadros sin modelos 3D (título, historia, menús, avisos)

Son imágenes planas pintadas a 4:3 que pueden traer texto en cualquier parte. Se muestran como en el
original, entre barras, y lo que el juego dibuja fuera de la imagen no se ve.
Parche: `aurora-wide-picture-flat-frames.patch`.

Un cuadro cuenta como 3D si el cuadro anterior dibujó al menos un modelo en perspectiva de más de
20 vértices; un cuadro no puede saber de antemano qué va a traer.

### Diagnóstico

Con F9, además del trazo de GX, el registro trae una línea `draw-extent:` por dibujo: si es plano o
3D, cuántos vértices tiene y de qué orilla a qué orilla llega en la imagen 4:3 (-1 a 1).
Parches: `aurora-draw-extents-log.patch` y `gx-draw-extents-log.patch`.

### Pendiente

- Lados difuminados para las escenas planas: en vez de barras negras, la misma imagen ampliada y
  borrosa.

## English

Trauma Center: Second Opinion is made for 4:3. With the wide picture option (F10 → Graphics → Wide
picture), the port decides frame by frame what to do with each draw.

### Frames with 3D models (the operations)

- **The 3D camera opens up.** The game keeps its 4:3 camera for its own work (where the wound, the
  sutures and the guide lines go), and only the GPU's copy is made wide. The body and the marks line
  up, and the sides show more of the operating room. Patch: `trauma-center-wide-camera.patch`.
- **Draws that cover the whole picture** (the blurred backdrop, tints over the scene) are enlarged
  evenly until they fill the frame: nothing is stretched, a little of the top and bottom is cut.
  Patch: `aurora-wide-picture-whole-pictures.patch`.
- **Bands across the picture** (the dark panel and the line at the bottom) are stretched sideways.
  Patch: `aurora-wide-picture-bands.patch`.
- **Bands built from several pieces** (the stripes at the top: left end, middle, right end): each end
  is pulled out to the frame's edge while its other side stays against the middle.
  Patch: `aurora-wide-picture-band-ends.patch`.
- **Everything else** (numbers, the tool hexagon, the nurse, the text) stays 4:3, in place.

### Frames without 3D models (title, story, menus, notices)

These are flat pictures painted at 4:3 that may carry text anywhere. They are shown as in the
original, between bars, and anything the game draws past the picture's edges stays hidden.
Patch: `aurora-wide-picture-flat-frames.patch`.

A frame counts as 3D when the frame before drew at least one perspective model of more than 20
vertices; a frame cannot know in advance what it will hold.

### Diagnostics

With F9, besides the GX trace, the log gets one `draw-extent:` line per draw: flat or 3D, how many
vertices, and from which edge to which it reaches in the 4:3 picture (-1 to 1).
Patches: `aurora-draw-extents-log.patch` and `gx-draw-extents-log.patch`.

### To do

- Blurred sides for flat scenes: instead of black bars, the same picture enlarged and blurred.
