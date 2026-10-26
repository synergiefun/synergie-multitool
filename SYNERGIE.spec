# PyInstaller spec for SYNERGIE Multitool (Windows console application).
from PyInstaller.utils.hooks import collect_all
import os

root = SPECPATH
all_datas = []
all_binaries = []
all_hiddenimports = []
for package in ("rich", "dns", "phonenumbers", "PIL"):
    datas, binaries, hiddenimports = collect_all(package)
    all_datas += datas
    all_binaries += binaries
    all_hiddenimports += hiddenimports

a = Analysis(
    [os.path.join(SPECPATH, "synergie_multitool.py")],
    pathex=[root],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="SYNERGIE",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    icon=os.path.join(root, "assets", "synergie.ico"),
)
