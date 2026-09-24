<#
    Start the appointment system on this machine.

    Seeds the sample data when needed, then runs the Flask development server
    on http://127.0.0.1:5000. Use -ResetDatabase to rebuild the sample data.
#>
param(
    [switch]$ResetDatabase
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$venvPython = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    throw "No virtual environment found. Run scripts\bootstrap.ps1 first."
}

if ($ResetDatabase) {
    & $venvPython "scripts\seed_data.py" --reset
}
else {
    & $venvPython "scripts\seed_data.py"
}

& $venvPython "run.py"
