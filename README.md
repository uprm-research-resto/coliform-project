#Coliform Project [![Build Status](https://travis-ci.org/Regendor/coliform-project.svg?branch=master)](https://travis-ci.org/Regendor/coliform-project) [![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](https://spdx.org/licenses/GPL-3.0.html)
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
    * [RPiCamera](#rpicamera)
    * [RPiGPIO](#rpigpio)
    * [GUI](#gui)
  * [Contact](#contact)

#Installation
For instructions on how to setup RPi watch: [Getting started with NOOBS](https://vimeo.com/90518800)

Before installing, you need to make sure you have [pip](https://pip.pypa.io/en/stable/installing/) installed, as it is required in order to install this module.

In Raspberry Pi, or Linux Type the following into terminal:
```bash
sudo pip3 install Coliform
```
If you are running the code on Linux, Windows or Mac PC, for testing or other purposes, you need to run the following code in terminal, or CMD depending on your OS:

Linux/Mac:
```bash
sudo pip install Coliform
```
Windows:
```bash
python -m pip install Coliform
```
Warning: As of version 0.5.3 only MultiPlot and ArduCAM libraries are compatible on systems other than RPi. 

#Requirements
* [pyserial](https://github.com/pyserial/pyserial) (only required if you need to use Arduino/ArduCAM)
* [Pillow](https://github.com/python-pillow/Pillow) (not required after version 0.5.3)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [picamera](https://github.com/waveform80/picamera)
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)

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
* Version 0.2.2
  - Minor Update:
    - Added GPL License classifiers.
* Version 0.3
  - Major Update:
    - Internal refactoring and cleaning up.
* Version 0.4
  - Major Update:
    - Merged Heater and Pump modules into a generic one called RPiGPIO
* Version 0.5b0 (Beta Version)
  - Major Update:
    - Added support for [picamera](https://github.com/waveform80/picamera), to use with our OV5647
    - Added corresponding GUI entries in order to get our results from OV5647
    - Began phasing out ArduCAM code
* Version 0.5b1 (Beta Version)
    - Added average intensity display to GUI
* Version 0.5b2 (Beta Version) (Deleted)
    - Corrupted package, was deleted.
* Version 0.5b3 (Beta Version)
    - Added intensity to location plot.
* Versions 0.5b4-7 (Beta Versions)
    - Fixed formatting errors and corrupted releases.
    - General debugging for new camera features
* Version 0.5.1b1 (Beta Version)
    - Stable tested release.
* Version 0.5.1
  - Minor Update:
    - Fixed minor errors in previous beta version
    - Has minor GUI formatting errors.
* Version 0.5.2
  - Minor Update:
    - Fixed formatting errors found in previous version.
* Version 0.5.3
  - Minor Update:
    - Fixed GUI formatting.
* Version 0.6
  - Major Update:
    - Canged intensity display range to 0-256
    - Fixed old formatting issues from OneWire module
    - Code restructuring for better fit good programming practices
    - Added image 'colorscaling' and functionality to various RPiCamera functions
    - Added more RPiCamera functions that better manage rgb data

#Usage
##Imports
The following imports are used:
```python
from Coliform import OneWire, Pump, ArduCAM, MultiPlot, Heater
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
from Coliform import OneWire

ids = OneWire.getOneWireID()
```
Where the values stored in ```ids``` will be a list with the addresses of the OneWires connected, for 2 OneWires:
```python
['/sys/bus/w1/devices/28-000005e2fdc3','/sys/bus/w1/devices/28-00000482b243']
```
These addresses change for each OneWire device.

In order to get temperature values the following code can be used:
```python
from Coliform import OneWire

TemperatureStringValues, TemperatureRawNumbers = OneWire.getTempList()
```
Where the first value, ```TemperatureStringValues``` is a string in the following format, for 3 OneWires:
```python
'21.312 C\n32.321 C\n43.232 C'
```
Which is displayed as:
```
   21.312 C
   32.321 C
   43.232 C
```
The second value ```TemperatureRawNumbers``` gives a list of temperature numbers, for 3 OneWires:
```python
['21.312','32.321','43.232']
```
##MultiPlot

##ArduCAM
```python
   from Coliform Import ArduCAM
   path = /home/
   filename = 'Test.jpg'
   portid = ArduCAM.getSerialPort()
   ArduCAM.TakePicture(path, portid[0], filename)
```

##RPiCamera
These functions use [picamera](https://github.com/waveform80/picamera), 
for more information on how to use the Camera and addtional usage, visit picamera [documentation](https://picamera.readthedocs.io/en/release-1.12/).

Here is a sample code to take a picture and show image taken. Current resolution is 1024 x 1008
```python
from Coliform import RPiCamera

# Takes picture after a 2 sec delay, and returns array to rgb_array variable
rgb_array = RPiCamera.takePicture()

# Show image taken
RPiCamera.showImage(rgb_array)


```

Now, to display an image with only green values in low light environment, we use:
```python
from Coliform import RPi.Camera

# Takes picture after a 30 sec delay, and returns array to rgb_array variable
# The following parameters are set: ISO(300), shutter speed(6 seconds), framerate(1/6), set exposure to off.
rgb_array_lowlight = RPiCamera.takePictureLow()

# Display only set color for the image, color choices are, for red: 'r' or 'red', green: 'g' or 'green', and blue: 'b' or 'blue'
# This requires an rgb image array, which is provided from the picture taken above and stored in rgb_array_lowlight
g_array = RPiCamera.setImageColor(rgb_array_lowlight, 'g')

# Displays image provided by the green rgb array. A 'greensacle' image
RPiCamera.showImage(g_array)

```

In order to get intensity values from the previous example, the following can be used:
```python
# Continuing from previous example
# Returns green intensity average value between range 0-256
green_intensity_avg = RPiCamera.returnIntensity(rgb_array_lowlight, 'g')

# Returns red intensity average value for the same range as described above
red_intensity_avg = RPiCamera.returnIntensity(rgb_array_lowlight, 'r')

# Returns blue intensity average value for the same range as described above
blue_intensity_avg = RPiCamera.returnIntensity(rgb_array_lowlight, 'b')

# Returns overall "Brightness" intensity value, for the same range as described above
overall_intensity_avg = RPiCamera.returnIntensity(rgb_array_lowlight, 'intensity')

# Or if we want to get all rgb and overall intensity values at the same time:
red_avg, green_avg, blue_avg, intensity_avg = RPiCamera.returnIntensity(rgb_array_lowlight)

# If we only want to get all rgb values at the same time:
red_avg, green_avg, blue_avg = RPiCamera.returnIntensity(rgb_array_lowlight, 'rgb')
```

In order to display plots containing histograms of red, green, blue raw data, along with redscale, greenscale, and bluescale images, we use the following:
```python
# Continuing from low light example
# Shows histograms and colorscaled images
RPiCamera.showPlot(rgb_array_lowlight)

```
```python
if RPiCamera.detectCamera():
    print('Camera is found')
else:
    print('Camera not found')
```

For further image processing, consider using [scipy](https://github.com/scipy/scipy) and [numpy](https://github.com/numpy/numpy) python libraries, for image manipulation as described here: [Advanced image processing using scipy and numpy](http://www.scipy-lectures.org/advanced/image_processing/)

##RPiGPIO
Both RPiGPIO use GPIO.PWM class from [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO). 
This is done in order to use software PWM to control pumps and Heaters.

In order to start the PWM control, and use it, the following code can be used:
```python
from Coliform import RPiGPIO
pin = 11 #RPi pin
frequency = 100 #start frequency

# Initialize the PWM controller
PWM = RPiGPIO.Controller(pin, frequency)

#Start PWM controller
PWM.startup()

#Start HeaterPID
PWM.HeaterPID()

freq = 50 # new frequency value
#change frequency within range
PWM.setIntensity(freq)

#Stop PWM
PWM.shutdown()
```

##GUI
In order to display the project GUI, the following code can be used:
```python
from Coliform import GUI

GUI.startGUI()
```
The GUI displayed should look like this:

![GUI](https://camo.githubusercontent.com/fec1ad443d25d345045462c50a307343fc3ff7a8/68747470733a2f2f7570726d7265736561726368726573746f2e66696c65732e776f726470726573732e636f6d2f323031362f30392f67756975706c6f616465642e706e673f773d373438)
