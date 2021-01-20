from setuptools import setup

APP = ['SportsBook.py']
APP_NAME = "NHL Prediction Calculator"
DATA_FILES = []
OPTIONS = {
	'packages': ['tkinter'],
    'iconfile':'Skating.icns',
    'plist': {
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