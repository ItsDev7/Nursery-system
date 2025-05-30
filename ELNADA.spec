from PyInstaller.utils.hooks import collect_submodules

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['./frontend'],
    binaries=[],
    datas=[
        ('images', 'images'),
        ('backend', 'backend'),
        ('frontend', 'frontend'),
        ('venv/Lib/site-packages/googleapiclient/discovery_cache/documents', 'googleapiclient/discovery_cache/documents'),
        ('credentials.json', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'arabic_reshaper',
        'bidi',
        'sqlalchemy',
        'google.oauth2.credentials',
        'google_auth_oauthlib.flow',
        'googleapiclient.discovery',
        'frontend',
        'frontend.registration',
        'frontend.registration.student_form',
        'frontend.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='نظام الحضانة',
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
    icon='images/Nursery-icon.ico'
) 