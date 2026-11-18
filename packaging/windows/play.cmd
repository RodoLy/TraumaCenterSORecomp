@echo off
rem Double-click to build the game from your disc and play. / Doble clic para compilar el juego desde tu disco y jugar.
rem Options go to play.ps1 (play.cmd -Rebuild, play.cmd -Disc D:\game.rvz). / Las opciones van a play.ps1.
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0play.ps1" %*
if errorlevel 1 pause
