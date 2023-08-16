# Unique
_The UUID & ULID Generator Tool_

- [UUIDs and ULIDs: An Introduction](#uuids-and-ulids-an-introduction)
  - [What is a UUID? (from Wikipedia)](#what-is-a-uuid-from-wikipedia)
  - [...and what is a ULID?](#and-what-is-a-ulid)
- [Installing and using _Unique_](#installing-and-using-unique)
  - [Graphical Installer](#graphical-installer)
  - [Graphical User Interface mode](#graphical-user-interface-mode)
  - [Command-line Interface mode](#command-line-interface-mode)
    - [UUID Generation](#uuid-generation)
      - [Usage examples (windows)](#usage-examples-windows)
      - [Usage examples (gnu/linux ubuntu)](#usage-examples-gnulinux-ubuntu)
      - [```unique.exe --help```: help and usage instructions](#uniqueexe---help-help-and-usage-instructions)
    - [ULID Generation](#ulid-generation)
      - [Usage examples (windows)](#usage-examples-windows-1)
      - [```unique.exe ulid --help```: help and usage instructions](#uniqueexe-ulid---help-help-and-usage-instructions)
    - [UUID Decoding](#uuid-decoding)
      - [Usage examples (windows)](#usage-examples-windows-2)
      - [```unique.exe decode --help```: help and usage instructions](#uniqueexe-decode---help-help-and-usage-instructions)
  - [Using CLI with Docker](#using-cli-with-docker)
    - [Build Docker Image](#build-docker-image)
    - [Run Docker Image (Examples)](#run-docker-image-examples)
    - [Docker running on Ubuntu 20.04 LTS in a VirtualBox VML](#docker-running-on-ubuntu-2004-lts-in-a-virtualbox-vml)
    - [Docker running on Debian "on the metal" through a SSH session](#docker-running-on-debian-on-the-metal-through-a-ssh-session)
- [How to compile and build the installer](#how-to-compile-and-build-the-installer)
  - [Python, venv, and Prerequisites](#python-venv-and-prerequisites)
  - [Compile .exe and build Installer](#compile-exe-and-build-installer)
  - [venv first-time use (reference-only)](#venv-first-time-use-reference-only)
- [Contributing to this Project](#contributing-to-this-project)
- [Security Policy for this Project](#security-policy-for-this-project)
- [Thanks \& Useful Links](#thanks--useful-links)
    - [People / Organisations](#people--organisations)
    - [Software](#software)
    - [Further Reading](#further-reading)
    - [Online Useful Links/Guides](#online-useful-linksguides)

## UUIDs and ULIDs: An Introduction
May 2016: I needed a random number generator and learned about UUIDs. This tool started as a way to automatically generate 20 v4 UUIDs (the only one not static or engineered to a set of hardware) and has since turned into a sandbox/demonstration project. Inside this repository you'll find a number of different technologies and concepts; from ```oid```'s and ```dns``` validation using Regular Expressions in the source code, up to ```venv``` and ```makensis``` to build and package the end solution. Hopefully this project serves as a good jumping-off point for someone wanting to learn ```git``` or ```python```.

As for that end-solution? This tools ships as both a graphical (notepad-like) application you can click through, as well as a lightning-fast utility leveraging syntax and principals from my favourite Unix software. This code is tested on Windows, Mac OS and Ubuntu and can also be run via Docker.

### What is a UUID? (from [Wikipedia](https://https://en.wikipedia.org/wiki/Universally_unique_identifier))
A Universally Unique IDentifier (UUID) is a 128-bit number used to identify information in computer systems. UUIDs are, for practical purposes, unique. Their uniqueness does not depend on a central registration authority or coordination between the parties generating them. Anyone can create a UUID and use it to identify something with near certainty that the identifier does not duplicate one that has already been, or will be, created to identify something else.

### ...and what is a ULID?
Unique Lexicographically Sortable Identifiers (ULIDs) are; like UUIDs, 128-bit random numbers used to to universally identify data items. With the added benefits of being shorter (26 character Base32-encoded string), sortable (lexicographically and monotonic) and case insensitive.

---
## Installing and using _Unique_

<img alt="unique's project icon" align="right" width="128px" src="src/icon/icon_source_vector.svg" />

Features
- Generate UUID Versions 1, 3, 4, 5 and the "Special Nil Case"/0 (_GUI 0/1/4 Only_)
- Support for DNS (FQDN), URL, OID and X.500 Namespaces (```--ns```)
- Prefix UUID with URN (RFC 4122) (```-u```)
- Command line Unix-Like tool and Graphical User Interface
- Non-Standard: Output UUID as Uppercase (```-U```)
- Shorten UUIDs using Base64 Encoding (```-s```)
- Use colourful syntax highlighting to understand UUIDs (```-c```)
- Decode UUID with pretty-print or version/type information
- Generation of Unique Lexicographically Sortable Identifiers / [ULIDs](https://github.com/mdipierro/ulid)
- Platform Agnostic: Python, Docker & Windows

### Graphical Installer
### Graphical User Interface mode
Using the ```tkinter``` library, a gui is available to generate UUIDs for those not comfortable with the command line. Simply click on your desktop link (windows) or open/execute ```python3 src/unique_gui.py``` (linux) to be presented with the graphical interface.

| &nbsp;     | Windows                                   | Linux                                     | macOS                                     |
| ---------- | ----------------------------------------- | ----------------------------------------- | ----------------------------------------- |
| __Unique__ | ![](.images/screenshot-win10.png)         | ![](.images/screenshot-linux.png)         | ![](.images/screenshot-macOS.png)         |
| Menu       | ![](.images/screenshot-win10-menu.png)    | ![](.images/screenshot-linux-menu.png)    | ![](.images/screenshot-macOS-menu.png)    |
| Options    | ![](.images/screenshot-win10-options.png) | ![](.images/screenshot-linux-options.png) | ![](.images/screenshot-macOS-options.png) |
| About      | ![](.images/screenshot-win10-about.png)   | ![](.images/screenshot-linux-about.png)   | ![](.images/screenshot-macOS-about.png)   |

The following Menu options are available:
* File
  * __New__: Clear-down the UUIDs in the current tool, ready for new generation (__CTRL + N__)
  * __Open__: Open a text (```.txt```/```.uuid```) file, useful for appending UUIDs (__CTRL + O__)
  * __Save__: Save the current UUIDs to a text (```.txt```/```.uuid```) file (__CTRL + S__)
  * __Save As..__: Save the current UUIDs to a new text (```.txt```/```.uuid```) file
  * __Quit__ (__ALT + F4__)
* Generate
  * __Version 1 UUID__: Generate a Version 1 (Datetime & MAC Address) UUID (__CTRL + 1__)
  * __Version 1 UUID__: Generate a Version 3 (Datetime & MAC Address) UUID (__CTRL + 3__)
  * __Version 4 UUID__: Generate a Version 4 UUID (based on RNG) (__CTRL + 4__)
  * __Version 1 UUID__: Generate a Version 5 (Datetime & MAC Address) UUID (__CTRL + 5__)
  * __Special Nil UUID__: Generate a Nil UUID (_0's_) (__CTRL + 0__)
  * __Special Nil UUID__: Generate a ULID (_0's_) (__CTRL + L__)
* Tools
  * __Options__: Open the Options popup (__F9__)
* Help
  * __About__: Opens a popup window with author/version information (__F1__)

### Command-line Interface mode
#### UUID Generation
##### Usage examples (windows)
```ps
# UUIDv4
unique.exe
'27fd1448-3c0d-4d73-94c4-9f16dd9e0c16'

# 3 x UUIDv4
unique.exe -q 3
'32ec9ca1-2a84-40c9-afa4-f67a7a8c3156'
'039ee9f1-c5a0-4d85-805a-89b84974a6c7'
'b6a4587d-a3de-4e4c-8d84-a3fad6b14192'

# 2 x UUIDv1 with URN prefix
unique.exe -v 1 -q 2 -u
'urn:uuid:7ed04b31-f14c-11ea-ac52-e4b31802edf0'
'urn:uuid:7ed0c3d9-f14c-11ea-aabd-e4b31802edf0'

# 1x Special Nil UUID
unique.exe -q 1 -v 0
'00000000-0000-0000-0000-000000000000'

# UUIDv5 for "python.org" Fully qualified domain name
unique.exe -v 5 --ns dns -n "python.org"
'886313e1-3b8a-5372-9b90-0c9aee199e5d'

# Uppercase UUIDv3 for "http://adambonner.co.uk" URL
unique.exe -U -v 3 -n "http://adambonner.co.uk" --ns url
'1FDC56DF-BB86-3F0D-9356-8612ABA227FF'
```

##### Usage examples (gnu/linux ubuntu)
```bash
# UUIDv4
python3 unique.py
'31c2c13c-60c9-4883-8f12-16ede5022da4'

# 3x UUIDv1 encoded as Base64
python3 unique.py -v 1 -q 3 --short
'EHuMMPxlEeqNuc2jzUq+xw=='
'EHuMMfxlEeqNuc2jzUq+xw=='
'EHuMMvxlEeqNuc2jzUq+xw=='
```

##### ```unique.exe --help```: help and usage instructions
```
usage: unique.py [-h] [-v <VERSION>] [-q <QUANTITY>] [--ns <NAMESPACE>] [-n <NAME>] [-c] [-u | -U | -s] {decode,ulid} ...

Generate or Decode a Universally Unique ID

positional arguments:
  {decode,ulid}         DECODE UUID or GENERATE a ULID

options:
  -h, --help            show this help message and exit
  -v <VERSION>, --version <VERSION>
                        Specify output UUID version (0, 1, 3, 4, or 5)
  -q <QUANTITY>, --quantity <QUANTITY>
                        Specify output quantity (1 - 65536)
  --ns <NAMESPACE>, --namespace <NAMESPACE>
                        UUID v3 or v5 namespace
  -n <NAME>, --name <NAME>
                        Specify UUID v3 or v5 name
  -c, --colour          Enable colour syntax highlighting
  -u, --urn             Specify URN standard prefix
  -U, --uppercase       Non-standard uppercase UUID string
  -s, --short           Shortened UUID using Base64 Encoding
```

#### ULID Generation
##### Usage examples (windows)
```ps
# Decode and Pretty-Print Base64 Encoded UUID
unique.exe decode EaLLP0e7R9akp4EC/wyw4w==
'11a2cb3f-47bb-47d6-a4a7-8102ff0cb0e3'

# Decode Base64 Encoded UUID with verbose information
unique.exe decode -i famfC///EeqRY6RMyKyUKg==
'Input String:   famfC///EeqRY6RMyKyUKg=='
'Input Type:     Base64'
'UUID:           7da99f0b-ffff-11ea-9163-a44cc8ac942a'
'Version:        1'
'Description:    Time and Node Based UUID'
'Namespace:      None'
'Name:           None'
'Date & Time:    2020-09-26 13:52:17.823309'
'MAC Address:    a4-4c-c8-ac-94-2a'
'Base64:         famfC///EeqRY6RMyKyUKg=='
'URN Prefix:     urn:uuid:7da99f0b-ffff-11ea-9163-a44cc8ac942a'
'Hexadecimal:    7da99f0bffff11ea9163a44cc8ac942a'
'Integer:        167034223496070676450392100360877282346'
'Uppercase:      7DA99F0B-FFFF-11EA-9163-A44CC8AC942A'
```

##### ```unique.exe ulid --help```: help and usage instructions
```
usage: unique.py ulid [-h] [-q <QUANTITY>]

options:
  -h, --help            show this help message and exit
  -q <QUANTITY>, --quantity <QUANTITY>
                        Specify output quantity (1 - 65536)
```

#### UUID Decoding
##### Usage examples (windows)
```ps
# Generate 5xULIDs
unique.exe ulid -q 5
'01EK645S91Q27M3343C2607VWY'
'01EK645S92V05X50AGX4BB337R'
'01EK645S93CTX4SE9TQJ03DQKA'
'01EK645S936YJ7CPR6ME36G44B'
'01EK645S9GM5RDNAT1YG6Z8AJV'
```

##### ```unique.exe decode --help```: help and usage instructions
```
usage: unique.py decode [-h] [-i] UUID

positional arguments:
  UUID               A valid (Hex|Base64|Uppercase|Prefixed) UUID string

options:
  -h, --help         show this help message and exit
  -i, --information  Provide detailed information about decoded UUID
```
### Using CLI with Docker
>__Note:__ The Docker (CLI-only) version of this project is inherently platform independent. This readme doesn't discuss that technology. Get started [here](https://docs.docker.com/get-started/).

The project's Dockerfile can be utilised to create a platform independent container image; supporting the generation of UUIDs in cloud (e.g. Kubernetes/OpenShift) environments. Getting ```unique``` to work with docker requires two steps, first create the docker image, then run it in the docker service

#### Build Docker Image
```bash
#Use Docker to Build Image, you may need elevated privilages/"root"
docker build . -t unique
```
#### Run Docker Image (Examples)

```bash
# UUIDv4
docker run --rm -it unique:latest
'513717ae-eb2e-4a06-9d5b-acaa77f7a6d7'

# 5 x UUIDv4
docker run --rm -it unique:latest -q 5
'32ec9ca1-2a84-40c9-afa4-f67a7a8c3156'
'039ee9f1-c5a0-4d85-805a-89b84974a6c7'
'b6a4587d-a3de-4e4c-8d84-a3fad6b14192'
'91bd7bf0-8b6e-46af-ad01-7f91ca66aa25'
'4085c90e-b195-40fb-b31e-e5faf76eb34a'

# Display Help
docker run --rm -it unique:latest --help
```

#### Docker running on Ubuntu 20.04 LTS in a VirtualBox VML
![](.images/screenshot-linux-ubuntu-docker.png)

#### Docker running on Debian "on the metal" through a SSH session
![](.images/screenshot-linux-debian-docker.png)

---
## How to compile and build the installer
### Python, venv, and Prerequisites
Virtual Environment Setup using your favourite terminal, from the project root directory:

```ps
# "create a virtual environment named venv"
py -m venv venv

# "activate the virtual environment"
'.\venv\Scripts\activate.ps1'

# "pip upgrade pip and setuptools"
py -m pip install --upgrade pip
py -m pip install --upgrade setuptools

# "install this project's dependencies"
py -m pip install -r '.\requirements.txt'
```

### Compile .exe and build Installer
Compile the .exe files using PyInstaller, and package them up with NSIS using your favourite terminal, from the project root directory:

```ps
# compile manually
pyinstaller 'src/unique.spec' --noconfirm

# package with nsis manually
makensis 'installer/unique.nsi'

# run both automatically
py 'tools/make.py'
```

### venv first-time use (reference-only)
using your favourite terminal, from the project root directory:

```ps
# "install this project's dependencies"
py -m pip install pyinstaller

# check prerequisites
py -m pip list --local

# record deps
pip freeze > 'requirements.txt'

# exit venv
deactivate
```

---
## Contributing to this Project
This project welcomes contributions of all types. We ask that before you start work on a feature that you would like to contribute, please read the [Contributor's Guide](.github/CONTRIBUTING.md).

---
## Security Policy for this Project
This project seeks to build secure, versatile and robust portable software. If you find an issue, please report it following the [Security Policy](.github/SECURITY.md)

---
## Thanks & Useful Links

#### People / Organisations
- [jatinkarthik-tripathy](https://github.com/jatinkarthik-tripathy/Text-Editor)'s Text Editor (in Python)
- [six519](https://github.com/six519/Python-Notepad)'s Python Notepad

#### Software
- The [NSIS](https://nsis.sourceforge.io/Main_Page) Project
- [Paint.net](https://getpaint.net/) for Image editing
- [IcoFx Portable](https://portableapps.com/apps/graphics_pictures/icofx_portable) for Icon file editing

#### Further Reading
- [Base64](https://en.wikipedia.org/wiki/Base64)
- [URN](https://en.wikipedia.org/wiki/Uniform_Resource_Name), [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier) and [URL](https://en.wikipedia.org/wiki/URL)
- [OID / object identifier](https://en.wikipedia.org/wiki/Object_identifier)
- [X.500 Distinguished Names](https://www.ibm.com/support/knowledgecenter/en/SSYKE2_7.0.0/com.ibm.java.security.component.70.doc/security-component/keytoolDocs/x500dnames.html)
- [MAC Address](https://www.ibm.com/support/knowledgecenter/en/SSYKE2_7.0.0/com.ibm.java.security.component.70.doc/security-component/keytoolDocs/x500dnames.html)


#### Online Useful Links/Guides
- [code-mentor.org](https://code-mentor.org/notepad-using-tkinter-in-python-with-source-code)
