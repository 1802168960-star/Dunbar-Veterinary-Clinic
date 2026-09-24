<#
    One-shot Windows setup for the Dunbar Veterinary Clinic appointment system.

    Creates the virtual environment, installs the requirements, copies
    .env.example to .env (when there is no .env yet) and seeds the database.

    Usage:
        powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
        powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -ResetDatabase
        powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -SkipSeed
#>
param(
    [switch]$SkipSeed,
    [switch]$ResetDatabase
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python was not found on PATH. Install Python 3.11 or newer first."
}

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating the virtual environment (.venv) ..."
    python -m venv .venv
}

$venvPython = Join-Path $root ".venv\Scripts\python.exe"

Write-Host "Installing dependencies ..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example - adjust SECRET_KEY before sharing this machine."
}

if (-not $SkipSeed) {
    if ($ResetDatabase) {
        Write-Host "Seeding the database (reset) ..."
        & $venvPython "scripts\seed_data.py" --reset
    }
    else {
        Write-Host "Seeding the database ..."
        & $venvPython "scripts\seed_data.py"
    }
}

Write-Host ""
Write-Host "Setup complete. Start the app with:"
Write-Host "    powershell -ExecutionPolicy Bypass -File scripts\run.ps1"
