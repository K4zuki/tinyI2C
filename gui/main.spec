# -*- mode: python -*-
a = Analysis(['\\\\tk-filer\\home_windows\\kyamamot\\common\\GitHub\\TinyI2C\\gui\\main.py'],
             pathex=['\\\\tk-filer\\home_windows\\kyamamot\\common\\GitHub\\TinyI2C\\gui'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='TinyI2C.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
