@echo off
REM This script builds the main.py into a single executable using PyInstaller

REM Delete build/ directory if it exists
if exist build (
    echo Deleting build/ directory...
    rmdir /s /q build
)

REM Delete dist/ directory if it exists
if exist dist (
    echo Deleting dist/ directory...
    rmdir /s /q dist
)

REM Delete main.spec file if it exists
if exist main.spec (
    echo Deleting main.spec file...
    del /q main.spec
)

REM Run PyInstaller with the necessary hidden imports
pyinstaller --onefile --hidden-import=fitz --hidden-import=pymupdf --hidden-import=tabulate --hidden-import=argparse --hidden-import=os main.py