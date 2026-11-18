Trauma Center: Second Opinion - native PC build (Windows)
=========================================================

Español abajo.

This package has no game in it. It builds the game on your computer from your own disc
(RKDEEB, the USA release), with WiiCompiled's runtime and no emulator.

THIS IS A FIRST TEST BUILD. It may not reach the title screen yet.

What you need
-------------
- Your disc image (.rvz, .iso, .wbfs, .wia or .ciso), the same one Dolphin plays. The
  script extracts it once to Disc\. A folder you already extracted with Dolphin (the one
  with sys\main.dol, sys\fst.bin and files\) works too.
- About 6 GB free: the extracted disc and the build.
- A short folder for this package, like C:\TCSO: the build makes long file names.

How to play
-----------
1. Unzip the package to C:\TCSO (or another short folder).
2. Double click play.cmd and choose your disc image.
3. It extracts the disc (once, a few minutes), translates the game (under a minute) and
   compiles it (a while the first time; much less after that), then starts it.

Settings, saves and logs are in UserData\. The disc image is remembered in
UserData\disc.txt. play.cmd -Rebuild builds everything again.

If the game stops, the window says why (often an address the native code does not know
yet in this game). Please report that message and the newest file in UserData\Logs.

Controls: with no real Wii Remote, the game gets an emulated Wii Remote with a
Nunchuk. The mouse is the pointer, left click A, right click B. Your gamepad or keyboard
works as the GameCube controller mapped in F10: stick = Nunchuk stick (choosing tools),
A/B = A/B, L/R = Z/C. A real Wii Remote can be paired in F10 instead.

Snapdragon X laptops: update the graphics driver first (Snapdragon Control Panel in the
Microsoft Store, or your laptop maker's support app). The game uses Direct3D 12 by default.


Trauma Center: Second Opinion - versión nativa para PC (Windows)
================================================================

Este paquete no trae el juego. Lo compila en tu computadora desde tu propio disco
(RKDEEB, la versión de Estados Unidos), con el runtime de WiiCompiled y sin emulador.

ESTA ES UNA PRIMERA VERSIÓN DE PRUEBA. Puede que todavía no llegue a la pantalla de título.

Qué necesitas
-------------
- Tu imagen del disco (.rvz, .iso, .wbfs, .wia o .ciso), la misma con la que juegas en
  Dolphin. El script la extrae una vez a Disc\. También sirve una carpeta que ya hayas
  extraído con Dolphin (la que tiene sys\main.dol, sys\fst.bin y files\).
- Unos 6 GB libres: el disco extraído y la compilación.
- Una carpeta corta para este paquete, como C:\TCSO: la compilación crea nombres de
  archivo largos.

Cómo jugar
----------
1. Descomprime el paquete en C:\TCSO (u otra carpeta corta).
2. Doble clic en play.cmd y elige la imagen de tu disco.
3. Extrae el disco (una sola vez, unos minutos), traduce el juego (menos de un minuto) y
   lo compila (un rato la primera vez; mucho menos después), y luego lo inicia.

La configuración, las partidas y los registros están en UserData\. La imagen del disco
se recuerda en UserData\disc.txt. play.cmd -Rebuild compila todo otra vez.

Si el juego se detiene, la ventana dice por qué (muchas veces una dirección que el código
nativo todavía no conoce en este juego). Reporta ese mensaje y el archivo más nuevo de
UserData\Logs.

Controles: sin un Wii Remote real, el juego recibe un Wii Remote con Nunchuk emulado.
El mouse es el puntero, clic izquierdo A, clic derecho B. Tu gamepad o teclado funciona
como el control de GameCube que mapeas en F10: stick = stick del Nunchuk (elegir
instrumentos), A/B = A/B, L/R = Z/C. En F10 también puedes emparejar un Wii Remote real.

Laptops Snapdragon X: primero actualiza el controlador gráfico (Snapdragon Control Panel
en la Microsoft Store, o la app de soporte del fabricante). El juego usa Direct3D 12.
