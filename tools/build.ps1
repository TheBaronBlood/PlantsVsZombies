param(
    [string]$VenvPython = ".venv\\Scripts\\python.exe",
    [string]$Name = "PlantsVsZombies"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $VenvPython)) {
    throw "Venv Python not found at '$VenvPython'. Activate the venv or pass -VenvPython."
}

& $VenvPython -m PyInstaller `
    --onefile `
    --noconsole `
    --name $Name `
    src\main.py `
    --add-data "assets;assets" `
    --add-data "src\settings.toml;src"
