# Fondos anchos / Wide backgrounds

## Español

Las escenas de historia usan fondos pintados a 4:3 (`files/sprite/bg/*.tpx`). Cada archivo es una
imagen de 1024×512 con 256 colores; el cuarto ocupa solo el centro (columnas 180 a 843, de las que
una pantalla 4:3 muestra de la 190 a la 833) y los lados son un color plano que nunca se ve.

`tools/wide_backgrounds.py` pinta esos lados como continuación del cuarto con LaMa, un modelo que
rellena partes faltantes de una imagen a partir de lo que las rodea. Lo que una pantalla 4:3 muestra
se queda exactamente igual: no se mueve ni se estira nada, solo se dibuja lo que estaba cortado. Los
colores nuevos se ajustan a los 256 del propio fondo, así que el archivo conserva su tamaño, su
formato y su paleta.

Los archivos del juego no se tocan y nada sacado del disco se sube a este repositorio: la
herramienta escribe los fondos nuevos en otra carpeta, junto con una vista previa de cómo se verían
en una pantalla 16:9.

```
python tools/wide_backgrounds.py <disco>/files/sprite/bg <carpeta de salida> --model big-lama.pt
```

Necesita numpy, pillow, torch y el modelo LaMa en TorchScript (`big-lama.pt`, por ejemplo de
https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt).

Pasos que faltan:

1. Revisar cada fondo generado.
2. Que el port entregue el fondo ancho cuando el juego lea el original, solo con pantalla ancha.
3. Que el fondo se dibuje a lo ancho, leyendo también sus lados, mientras personajes y texto siguen
   en 4:3.

## English

Story scenes use backgrounds painted at 4:3 (`files/sprite/bg/*.tpx`). Each file is a 1024×512
picture with 256 colours; the room only fills the middle (columns 180 to 843, of which a 4:3 screen
shows 190 to 833) and the sides are a flat colour that is never shown.

`tools/wide_backgrounds.py` paints those sides as a continuation of the room with LaMa, a model that
fills in missing parts of a picture from what surrounds them. What a 4:3 screen shows stays exactly
as it was: nothing is moved or stretched, only what was cut off is drawn. The new colours are matched
to the background's own 256, so the file keeps its size, its format and its palette.

The game files are not changed and nothing taken from the disc goes into this repository: the tool
writes the new backgrounds to another folder, together with a preview of how they would look on a
16:9 screen.

```
python tools/wide_backgrounds.py <disc>/files/sprite/bg <output folder> --model big-lama.pt
```

It needs numpy, pillow, torch and the LaMa model as TorchScript (`big-lama.pt`, for example from
https://github.com/Sanster/models/releases/download/add_big_lama/big-lama.pt).

Steps left:

1. Review every generated background.
2. Have the port hand over the wide background when the game reads the original, with the wide
   picture on only.
3. Draw the background across the wide frame, reading its sides too, while characters and text stay
   4:3.
