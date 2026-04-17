$venv = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $venv)) {
    Write-Error 'No se encontró .venv\Scripts\python.exe. Cree el entorno virtual con: python -m venv .venv'
    exit 1
}
& $venv run.py @args
