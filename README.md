# Unique
_The UUID & ULID Generator Tool_

## Virtual Environment, PyInstaller, and NSIS Installer Instructions

<details><!------------------------------------------------------------>
<summary>Virtual Environment Setup</summary>
using your favourite terminal, from the project root directory:

```ps
# "create a virtual environment named venv"
python -m venv venv

# "activate the virtual environment"
.\venv\Scripts\activate.ps1

# "pip upgrade pip and setuptools"
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# "install this project's dependencies"
pip install -r .\requirements.txt
```
</details>

<details><!------------------------------------------------------------>
<summary>Compile the .exe files using PyInstaller</summary>
using your favourite terminal, from the project root directory:

```ps
# "execute the following script for pyinstaller and makensis"
python .\tools\make.py
```
</details>


<details><!------------------------------------------------------------>
<summary>First-time Installation & Setup Details</summary>
using your favourite terminal, from the project root directory:

```ps
# "update python"
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# "create a virtual environment named venv"
python -m venv venv

# "activate the virtual environment"
.\venv\Scripts\activate.ps1

# "pip upgrade pip and setuptools"
python -m pip install --upgrade pip
python -m pip install --upgrade setuptools

# "install this project's dependencies"
python -m pip install pyinstaller

# check prerequisites
pip list --local

# record deps
pip freeze > requirements.txt

# exit venv
deactivate

# remove venv
rm -rf venv
```

</details>
















