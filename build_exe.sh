#!/bin/sh
# Build the Stardew Valley save editor into an executable using PyInstaller

SCRIPT="星露谷存档修改器_完整版.py"
pyinstaller --clean --onefile --windowed "$SCRIPT"
