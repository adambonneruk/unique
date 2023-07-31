# Unique
_The UUID & ULID Generator Tool_

### First Time Installation & Setup
```ps
# update python
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# install venv
python -m venv venv
.\venv\Scripts\activate.ps1

# update python in venv
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# install prereqs
python -m pip install pyinstaller

# check prereqs
pip list --local

# record deps
pip freeze > requirements.txt
```

### venv
```ps
# create and start venv
python -m venv venv
.\venv\Scripts\activate.ps1

# upgrade pip
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# install deps
pip install -r .\requirements.txt
```

### compile
```ps
# compile exe's with pyinstaller
py .\tools\make.py

# execute new .exe
.\dist\unique\unique.exe
```