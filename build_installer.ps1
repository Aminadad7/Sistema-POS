param(
    [string]$PythonExe = ".\.venv\Scripts\python.exe",
    [string]$IsccPath = ""
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

function Resolve-IsccPath {
    param(
        [string]$PreferredPath = ""
    )

    if ($PreferredPath -and (Test-Path $PreferredPath)) {
        return (Resolve-Path $PreferredPath).Path
    }

    $command = Get-Command "ISCC.exe" -ErrorAction SilentlyContinue
    if ($command -and $command.Source -and (Test-Path $command.Source)) {
        return $command.Source
    }

    $candidates = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "${env:ProgramFiles(x86)}\Inno Setup 5\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 5\ISCC.exe"
    )

    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return $candidate
        }
    }

    $regKeys = @(
        "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1",
        "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Inno Setup 6_is1"
    )

    foreach ($key in $regKeys) {
        if (-not (Test-Path $key)) {
            continue
        }

        $entry = Get-ItemProperty -Path $key -ErrorAction SilentlyContinue
        if (-not $entry) {
            continue
        }

        $fromInstallLocation = Join-Path ($entry.InstallLocation) "ISCC.exe"
        if ($entry.InstallLocation -and (Test-Path $fromInstallLocation)) {
            return $fromInstallLocation
        }

        if ($entry.DisplayIcon) {
            $displayIconPath = ($entry.DisplayIcon -split ',')[0].Trim('"')
            if ($displayIconPath -and (Test-Path $displayIconPath)) {
                $possibleFromIcon = Join-Path (Split-Path -Parent $displayIconPath) "ISCC.exe"
                if (Test-Path $possibleFromIcon) {
                    return $possibleFromIcon
                }
            }
        }
    }

    $lnkCandidates = @(
        (Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\Inno Setup 6\Inno Setup Compiler.lnk"),
        (Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Inno Setup 6\Inno Setup Compiler.lnk")
    )

    foreach ($lnkPath in $lnkCandidates) {
        if (-not (Test-Path $lnkPath)) {
            continue
        }

        try {
            $shell = New-Object -ComObject WScript.Shell
            $shortcut = $shell.CreateShortcut($lnkPath)
            $target = $shortcut.TargetPath
            if ($target -and (Test-Path $target)) {
                $possibleFromShortcut = Join-Path (Split-Path -Parent $target) "ISCC.exe"
                if (Test-Path $possibleFromShortcut) {
                    return $possibleFromShortcut
                }
            }
        }
        catch {
            continue
        }
    }

    return $null
}

if (-not (Test-Path $PythonExe)) {
    throw "No se encontro Python del entorno virtual en '$PythonExe'."
}

Write-Host "[1/3] Generando build con PyInstaller..." -ForegroundColor Cyan
$distPath = Join-Path $root "dist_installer"
$workPath = Join-Path $root "build_installer"

if (Test-Path $distPath) {
    Remove-Item $distPath -Recurse -Force
}
if (Test-Path $workPath) {
    Remove-Item $workPath -Recurse -Force
}

& $PythonExe -m PyInstaller run.spec --noconfirm --distpath $distPath --workpath $workPath
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller fallo con codigo $LASTEXITCODE"
}

$iscc = Resolve-IsccPath -PreferredPath $IsccPath

if (-not $iscc) {
    throw 'No se encontro ISCC.exe (Inno Setup). Instala Inno Setup 6 o ejecuta: .\build_installer.ps1 -IsccPath "C:\Ruta\ISCC.exe"'
}

Write-Host "[2/3] Compilando instalador con Inno Setup..." -ForegroundColor Cyan
Write-Host "Usando ISCC: $iscc" -ForegroundColor DarkGray
& $iscc "installer\SistemaPOS.iss"
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup fallo con codigo $LASTEXITCODE"
}

Write-Host "[3/3] Instalador generado correctamente." -ForegroundColor Green
Write-Host "Salida: installer\output\SistemaPOS-Setup.exe" -ForegroundColor Green
