# Stardew Valley Save Editor

This repository contains a simple Stardew Valley save editor written in Python with PyQt5.

## Requirements

- Python 3.8 or higher
- PyQt5 (install via `pip install -r requirements.txt`)
- PyInstaller (for packaging to an executable)

## Usage

To run the editor directly:

```bash
pip install -r requirements.txt
python 星露谷存档修改器_完整版.py
```

## Building an executable

If you wish to package the application into a standalone executable, install `PyInstaller` and run the provided script:

```bash
pip install pyinstaller
./build_exe.sh
```

If `pyinstaller` is not available (for example due to network restrictions), the
build script will fail. Ensure PyInstaller is installed before running the
script.

The resulting executable will be placed in the `dist/` directory.

