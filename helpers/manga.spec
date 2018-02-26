# -*- mode: python -*-

block_cipher = None


added_files = [
    ('src/gui/langs', 'src/gui/langs'),
]


a = Analysis(['.builder.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['PIL.ImageQt'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='manga',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
