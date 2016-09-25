#Coliform Project [![Build Status](https://travis-ci.org/Regendor/coliform-project.svg?branch=master)](https://travis-ci.org/Regendor/coliform-project)
Python module for the UPRM BioMEMS Research Laboratory water quality project.

Written for Raspberry Pi(RPi) in Python 3.

Download page: [![PyPI Version](https://img.shields.io/pypi/v/coliform.svg)](https://pypi.python.org/pypi/Coliform)



#Table of contents

* [Coliform Project](#coliform-project)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
  * [Requirements](#requirements)
  * [Changelog](#changelog)
  * [Usage](#usage)
    * [Imports](#imports)
    * [OneWire](#onewire)
    * [MultiPlot](#multiplot)
    * [ArduCAM](#arducam)
    * [GPIO](#gpio)
    * [GUI](#gui)
  * [Contact](#contact)

#Installation

Before installing, you need to make sure you have [pip](https://pip.pypa.io/en/stable/installing/) installed, as it is required in order to install this module.

In Raspberry Pi, or Linux Type the following into terminal:
```bash
sudo pip3 install Coliform
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
The reason is you need [fakeRPiGPIO](https://github.com/ArmlessJohn404/fakeRPiGPIO) module in order to "emulate" the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) module of the RPi.

Alternatively, you can download the python wheel package from [Coliform PyPI](https://pypi.python.org/pypi/Coliform) and python source from [fakeRPiGPIO PyPI](https://pypi.python.org/pypi/fakeRPiGPIO)

#Requirements
* [pyserial](https://github.com/pyserial/pyserial)
* [Pillow](https://github.com/python-pillow/Pillow)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) (when running on RPi) or [fakeRPiGPIO](https://github.com/ArmlessJohn404/fakeRPiGPIO) (when not running on RPi)

#Changelog
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

#Usage
##Imports
The following imports are used:
```python
from Coliform import *
from Coliform import GUI
```
The first is for all functions, but the GUI, and the second is to import the GUI function.
##OneWire
###Setup
These group of functions allow you to detect one or multiple OneWires, get their address and display their respective temperature. This code was written and tested for [DS18B20](https://www.maximintegrated.com/en/products/analog/sensors-and-sensor-interface/DS18B20.html/tb_tab0) OneWires.

If multiple OneWires are connected, they need to be in the following configuration:
![OneWire Connection](https://camo.githubusercontent.com/99c16972ad946ec3d40c29d4999fdc90600728ac/68747470733a2f2f7570726d7265736561726368726573746f2e66696c65732e776f726470726573732e636f6d2f323031362f30392f6f6e657769726572706973657475702e706e673f773d34383326683d363431)

Where black, is ground, red is power (3.3V), and yellow is the digital signal. You also need a 4.7kΩ resistor connected as shown. All yellow (signal) cables send their signal to the GPIO4 pin of the RPi.

In order to detect OneWires, using the w1-gpio kernel driver, the GPIO4 pin has to be setup to recieve the information from them, in order to do this open the RPi terminal and do the following:

* Type: ```sudo nado /boot/config.txt```
* Add: ```dtoverlay=w1-gpio,gpiopin=4``` to the end of the file.
* Press: ```Ctrl + X``` followed by ```y``` and ```ENTER``` or ```RETURN```
* After this, type: ```sudo reboot``` and wait for RPi to reboot, for changes to be applied.

###Code
In order to get OneWire address, use the following function:
```python
from Coliform import *

ids = getOneWireID()
```
Where the values stored in ```ids``` will be a list with the addresses of the OneWires connected, for 2 OneWires:
```python
['/sys/bus/w1/devices/28-000005e2fdc3','/sys/bus/w1/devices/28-00000482b243']
```
These addresses change for each OneWire device.

In order to get temperature values the following code can be used:
```python
from Coliform import *

TemperatureStringValues, TemperatureRawNumbers = getTempList()
```
Where the first value, ```TemperatureStringValues``` is a string in the following format, for 3 OneWires:
```python
'21.312\n32.321\n43.232'
```
Which is displayed as:
```
   21.312
   32.321
   43.232
```
The second value ```TemperatureRawNumbers``` gives a list of temperature numbers, for 3 OneWires:
```python
['21.312','32.321','43.232']
```
