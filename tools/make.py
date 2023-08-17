""" make.py is a tool script used to...
	(1) compile the solution with PyInstaller
    (2) package this with NSIS
"""

import os

print("make.py: compile and package installer")

# compile gui solution, overwrite existing files (in build/dist folders) using predefined .spec file
print("\n----------------------\npyinstaller src/unique_gui.spec --noconfirm")
os.system("pyinstaller src/unique_gui.spec --noconfirm")

# compile cli solution, overwrite existing files (in build/dist folders) using predefined .spec file
print("\n----------------------\npyinstaller src/unique.spec --noconfirm")
os.system("pyinstaller src/unique.spec --noconfirm")

# use nsis to build standard windows looking installer (and uninstaller)
print("\n----------------------\nmakensis installer/unique.nsi")
os.system("makensis installer/unique.nsi")