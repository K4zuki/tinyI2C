# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/yamamoto/workspace/tinyI2C/gui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='tinyI2C',
          debug=False,
          strip=None,
          upx=True,
          console=True )
