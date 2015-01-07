# -*- mode: python -*-
a = Analysis(['C:\\Users\\kyamamot\\Documents\\eagle\\TinyI2C\\gui\\main.py'],
#             pathex=['C:\\Users\\kyamamot\\Documents\\eagle\\TinyI2C\\gui','W:\\Tokyo\\Home\\kyamamot\\common\\GitHub\\tempcommand\\'],
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
          console=False )
