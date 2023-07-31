import os

print("working dir:")
os.system("pwd")

print("make file automation for unique cli version")
os.system("pyinstaller .\\src\\unique.spec --noconfirm")

os.system("echo.")

print("make file automation for unique gui version")
os.system("pyinstaller .\\src\\unique_gui.spec --noconfirm")