from setuptools import setup

APP = ['test.py']
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,  # Hide from Dock
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)