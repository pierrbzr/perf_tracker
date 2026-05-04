@echo off
:: Récupère le dossier où se trouve ce script (chemin relatif au disque)
set "PROJECT_DIR=%~dp0"

:: Patch le venv pour pointer vers le bon Python local de la machine
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i" && goto found
:found

:: Réécrit le pyvenv.cfg avec le bon home
echo home = %PYTHON_PATH:python.exe=% > "%PROJECT_DIR%.venv\pyvenv.cfg"
echo include-system-site-packages = false >> "%PROJECT_DIR%.venv\pyvenv.cfg"

:: Active le venv
call "%PROJECT_DIR%.venv\Scripts\activate.bat"
echo [OK] Environnement active depuis %PROJECT_DIR%