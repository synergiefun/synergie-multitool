@echo off
setlocal
cd /d "%~dp0"
echo ==============================================
echo        SYNERGIE - BUILD WINDOWS EXE
echo ==============================================
py -m pip install --upgrade pip
if errorlevel 1 goto error
py -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto error
py -m PyInstaller --clean --noconfirm SYNERGIE.spec
if errorlevel 1 goto error
echo.
echo Build termine : dist\SYNERGIE.exe
pause
exit /b 0
:error
echo.
echo Echec de la compilation. Verifiez Python, pip et votre connexion Internet.
pause
exit /b 1
