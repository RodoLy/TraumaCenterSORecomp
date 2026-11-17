# Trauma Center: Second Opinion – port nativo para PC

[English](README.md)

Un port nativo para PC de *Trauma Center: Second Opinion* (Wii) por recompilación estática, en
camino: el código PowerPC del juego se traducirá a C++ y se compilará para tu computadora, sin
emulador. Sigue el mismo camino que el
[port de *Harvest Moon: Animal Parade*](https://github.com/RodoLy/HarvestMoonAnimalParadeRecomp).

> **Recién empieza.** Todavía no se puede jugar. La fase 0, el mapa de funciones, ya está; lo
> siguiente es que el juego corra con DolRecomp y ModernGekko ([docs/PLAN.md](docs/PLAN.md)).

**Este repositorio no contiene datos del juego.** Necesitas tu propio disco: `Trauma Center:
Second Opinion (USA)`, ID `RKDEEB`.

## Lo que se planea

- Nativo en Windows x64 y Windows en ARM.
- Sin Wii Remote: el mouse es el puntero y el Nunchuk va al control o al teclado.
- Resolución alta y un mod opcional de pantalla ancha (el juego original solo es 4:3).
- Por defecto, todo se ve y se juega como en el Wii.

## Fase 0: el mapa de funciones del juego

Lo que necesitas: Python 3.11 o más nuevo y tu disco como imagen `.rvz` (el formato de Dolphin).

1. Instala las dependencias de las herramientas:

   ```sh
   pip install -r requirements-dev.txt
   ```

2. Saca los archivos de sistema de tu disco:

   ```sh
   python3 tools/extract_system_files.py "Trauma Center - Second Opinion (USA).rvz"
   ```

   Escribe `orig/RKDEEB/sys/boot.bin`, `main.dol` y `fst.bin`. Nada de `orig/` se sube nunca. El
   disco europeo también funciona y queda en `orig/RKDP01/`.

3. Comprueba el disco:

   ```sh
   python3 tools/check_disc.py
   ```

   Debe terminar con `OK: this is the target binary.`

4. Genera el mapa de funciones:

   ```sh
   python3 tools/analyze.py
   ```

   Escribe `config/RKDEEB/symbols.txt`, la única lista de nombres y tamaños de funciones que leen
   todas las demás herramientas. Después nombra las funciones del SDK de Nintendo con la base de
   datos de firmas de Dolphin (`Sys/totaldb.dsy` en tu carpeta de Dolphin):

   ```sh
   python3 tools/sdk_signatures.py --database ruta/a/totaldb.dsy --apply
   ```

   Lo que salió está en [docs/FUNCTION_MAP.md](docs/FUNCTION_MAP.md).

5. Corre las pruebas cuando quieras con `python3 -m pytest`. Arman archivos DOL mínimos a mano,
   así que no necesitan datos del juego.

## Agradecimientos

- [WiiCompiled](https://github.com/patchzyy/wiicompiled) y
  [ModernGekko](https://github.com/ExpansionPak/ModernGekko-Template) con DolRecomp, las
  herramientas de recompilación sobre las que se construye este port.
- [aurora](https://github.com/encounter/aurora) y [decomp-toolkit](https://github.com/encounter/decomp-toolkit).
- Atlus, por el juego. Este es un proyecto de fans no oficial, sin relación con Atlus, Sega ni
  Nintendo, ni respaldado por ellos.

## Licencia

GPL-3.0 (ver [LICENSE](LICENSE)). La licencia cubre solo el código de este repositorio; no da
ningún derecho sobre el juego.
