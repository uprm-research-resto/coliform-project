Coliform Project
=================
Python module for the UPRM BioMEMS Research Laboratory water quality project.
Written for Raspberry Pi(RPi) in Python 3.
Download page: https://pypi.python.org/pypi/Coliform

Table of contents
=================
* [Coliform Project](#coliform-project)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Requirements](#requirements)
  * [Changelog](#changelog)
  * [Usage](#usage)
    * [OneWire](#onewire)
    * [MultiPlot](#multiplot)
    * [ArduCAM](#arducam)
    * [GPIO](#gpio)
    * [GUI](#gui)
  * [Contact](#contact)

Installation
=================
In Raspberry Pi, or Linux Type the following into terminal:
```bash
sudo pip install Coliform
```
If you are running the code on Linux, Windows or Mac PC, for testing or other purposes, you need to run the following code in terminal, or CMD depending on your OS:

Linux/Mac:
```bash
sudo pip install Coliform
sudo pip install fakeRPiGPIO
```
Windows:
```bash
python -m pip install fakeRPiGPIO
python -m pip install Coliform
```
The reason is you need [fakeRPiGPIO](https://github.com/ArmlessJohn404/fakeRPiGPIO) module in order to "emulate" the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) module of the Raspberry Pi.

Alternatively, you can download the python wheel package from [Coliform PyPI](https://pypi.python.org/pypi/Coliform) and python source from [fakeRPiGPIO PyPI](https://pypi.python.org/pypi/fakeRPiGPIO)

Requirements
=================
* [pyserial](https://github.com/pyserial/pyserial)
* [Pillow](https://github.com/python-pillow/Pillow)
* [matplotlib](https://github.com/matplotlib/matplotlib)

Changelog
=================
* Version 0.1
  - Initial Build 
* Version 0.1.1
  - Minor Update: 
    - Added install requirements to wheel package
* Version 0.2
  - Major Update: 
    - Added MultiPlot and GPIO
    - Revamped OneWire and ArduCAM
    - Added PyPI Cassifiers
* Version 0.2.1
  - Minor Update:
    - Transfered Project GUI into Coliform module

Usage
=================
```python

```
