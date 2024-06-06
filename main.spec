# YourAppName.spec

# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.versioninfo import Version

# Additional imports for version file
import os

block_cipher = None

# Add version info
version_info = Version(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # The rest of the fields are optional
    desc='调试软件',
    comments='应用程序',
    company_name='奥创',
    legal_copyright='奥创',
    legal_trademarks='1, 0, 0, 0',
    product_name='调试软件',
)

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=collect_data_files('your_package_name'),  # Adjust if needed
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

# Create the version file
version_file = 'version.txt'
with open(version_file, 'w') as vf:
    vf.write(str(version_info))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='YourAppName',  # Set your application name here
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want a console window
    icon='path_to_your_icon.ico',  # Optional: Path to your .ico file
    version=version_file  # Add version file here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='YourAppName'  # Set your application name here
)
