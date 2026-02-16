# Plants vs Zombies (Fan Learning Project) 
![Python](https://img.shields.io/badge/python-3.12-blue.svg) ![Repo Size](https://img.shields.io/github/repo-size/Sulstice/global-chem)
![Static Badge](https://img.shields.io/badge/package-Arcade-blue?style=flat)

Simple Arcade-based fan project for learning game development in Python.
 
## Description
This project is a small, learning-focused clone inspired by EA/PopCap's Plants vs. Zombies.
It is not affiliated with or endorsed by EA or PopCap. The goal is to build a simple
menu → game → death flow with a few levels that can be extended later.

## Getting Started

### Dependencies
- Windows 10/11 (recommended), macOS, or Linux
- Python 3.11+ recommended
- `pip`

### Installing
1) Clone the repo.
2) Create a virtual environment.
3) Install dependencies.

```shell
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
Set-ExecutionPolicy -Scope Process -Execution Policy Bypass # Windows   
.venv\Scripts\activate                                      # Windows   
python -m pip install -r requirements.txt
```

### Executing program
```shell
python -m src.main
```

### Tests (optional)
```shell
pytest
```

### Build (optional)
Create a standalone exe with PyInstaller:
```shell
python -m pip install pyinstaller
pyinstaller --onefile --noconsole src/main.py
```
Or use the provided PowerShell build script (recommended):
```powershell
.\tools\build.ps1
```
Custom venv python or output name:
```powershell
.\tools\build.ps1 -VenvPython "D:\Path\python.exe" -Name "PvZ"
```

## Help
If you see missing-module errors, re-check that your venv is activated and
`requirements.txt` was installed.


## License
This project is licensed under the MIT License. See `LICENSE`.

## Acknowledgments
- Inspired by EA/PopCap's Plants vs. Zombies
