from setuptools import setup

APP = ['SportsBook.py']
APP_NAME = "NHL Prediction Calculator"
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
	'packages': ['tkinter', 'pandas', 'lxml', 'numpy', 'statistics', 'macholib'],
    'includes': ['tkinter', 'pandas', 'lxml', 'numpy', 'statistics', 'macholib'],
    'iconfile':'Skating.icns',
    'plist': {
        'PyRuntimeLocations': ['@executable_path/../Frameworks/libcrypto.1.1.dylib',
                               '@executable_path/../Frameworks/libncursesw.5.dylib',
                               '@executable_path/../Frameworks/libssl.1.1.dylib',
                               '@executable_path/../Frameworks/libtcl8.6.dylib',
                               '@executable_path/../Frameworks/libtk8.6.dylib'],
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Gettin' Rich",
        'CFBundleVersion': '1.0.1',
        'CFBundleShortVersionString': '1.0.1',
        'NSHumanReadableCopyright': u"Copyright © 2021, Jimbo Gilstrap, All Rights Reserved",
    }
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)