Coliform Project
=================
Python module for the UPRM BioMEMS Research Laboratory water quality project.
Written for Raspberry Pi(RPi) in Python 3.
PyPI Library link:https://pypi.python.org/pypi/Coliform

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
  * [Dependency](#dependency)

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
```python

```
Changelog
=================
* Version 0.1
* Version 0.1.1
* Version 0.2
* Version 0.2.1
