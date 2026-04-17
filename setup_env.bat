@echo off
setlocal
if exist .venv\Scripts\python.exe (
    echo El entorno virtual ya existe.
) else (
    echo Creando entorno virtual .venv...
    python -m venv .venv
)
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error instalando dependencias.
    exit /b %ERRORLEVEL%
)
echo Entorno preparado. Usa: .venv\Scripts\python.exe run.py
