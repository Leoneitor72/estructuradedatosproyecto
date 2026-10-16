@echo off
REM =========================================================================
REM Script de Compilacion y Empaquetado a Win32 EXE (Semana 3 - Dia 4)
REM Genera el ejecutable nativo para Windows mediante PyInstaller.
REM =========================================================================

echo [1/3] Verificando dependencias de empaquetado...
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo [INFO] PyInstaller no detectado. Instalando PyInstaller...
    python -m pip install pyinstaller
)

echo [2/3] Compilando Sistema de Gestion de Estudiantes a EXE independiente...
pyinstaller --noconfirm --onefile --windowed --name "SistemaEstudiantes" ^
  --add-data "models;models" ^
  --add-data "controllers;controllers" ^
  --add-data "views;views" ^
  app.py

if %errorlevel% equ 0 (
    echo.
    echo =========================================================================
    echo [EXITO] Compilacion completada con exito!
    echo El ejecutable independiente se encuentra en: dist\SistemaEstudiantes.exe
    echo =========================================================================
) else (
    echo.
    echo [ERROR] Hubo un problema durante la compilacion.
)
pause
