# -*- mode: python -*-
a = Analysis(['compressed.pyw'],
             pathex=['D:\\adri\\work\\PycharmProjects\\compressed_img'],
             hiddenimports=['atexit'],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Compressed.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
