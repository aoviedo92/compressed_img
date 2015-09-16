# -*- coding: utf-8 -*-
from distutils.core import setup
import py2exe
setup(
    windows=[
        {
            "script": "compressed.pyw",
            "icon_resources": [(0, "icon.ico"), (1, "icon.ico")]
        }
    ],
    # data_files = [
    #     (
    #         'imageformats', [r'C:\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll']
    #     )
    # ],

    options = {
        "py2exe": {
            'bundle_files': 1,
            'compressed': True,
            "dll_excludes": ["MSVCP90.dll"],
            "includes":["sip","PyQt4.QtGui","PyQt4.QtCore"]
        }
    },
    zipfile = None,
    name="compress_img",
    version="1.0",
    description="comprime las img de una carpeta.",
    author="Adrian Oviedo",
)


