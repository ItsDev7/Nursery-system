# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('frontend', 'frontend'), ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\arabic_reshaper', 'arabic_reshaper'),
     ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\bidi', 'bidi'),
      ('backend', 'backend'),
       ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\matplotlib', 'matplotlib'),
       ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\pyparsing', 'pyparsing'),
       ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\cycler', 'cycler'),
       ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\dateutil', 'dateutil'),
       ('E:\\Projects\\Elnada_project\\venv\\Lib\\site-packages\\kiwisolver', 'kiwisolver')],
        

    hiddenimports=['arabic_reshaper', 'bidi', 'configparser', 'sqlite3', 'uuid', 'six'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['venv', '__pycache__'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EL-NADA Nursery',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['images\\ELNADA-icon.ico'],
)
