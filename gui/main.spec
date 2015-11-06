# -*- mode: python -*-

block_cipher = None

a = Analysis(['\\\\tk-filer\\home_windows\\kyamamot\\common\\GitHub\\TinyI2C\\gui\\main.py'],
             pathex=['\\\\tk-filer\\home_windows\\kyamamot\\common\\GitHub\\TinyI2C\\gui','\\\\tk-filer\\home_windows\\kyamamot\\common\\GitHub\\TinyI2C\\python'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None
             )
#             ,
#             excludes=None,
#             cipher=block_cipher)
pyz = PYZ(a.pure)
#              ,
#             cipher=block_cipher)
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
#coll = COLLECT(exe,
#               a.binaries,
#               a.zipfiles,
#               a.datas,
#               strip=None,
#               upx=True,
#               name='main')
