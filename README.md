#Coliform Project [![Build Status](https://travis-ci.org/Regendor/coliform-project.svg?branch=master)](https://travis-ci.org/Regendor/coliform-project) [![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](https://spdx.org/licenses/GPL-3.0.html)
Python module for the UPRM BioMEMS Research Laboratory water quality project.

Written for Raspberry Pi(RPi) in Python 3.

Download page: [![PyPI Version](https://img.shields.io/pypi/v/coliform.svg)](https://pypi.python.org/pypi/Coliform)

For information about packaging and distributing your library to PyPi: [Packaging and Distributing Guide](https://packaging.python.org/distributing/)

#Table of contents

* [Coliform Project](#coliform-project)
  * [Table of contents](#table-of-contents)
  * [Installation](#installation)
    * [Setup RPi and install Coliform library](#setup-rpi-and-install-coliform-library)
  * [Requirements](#requirements)
  * [Changelog](#changelog)
  * [Usage](#usage)
    * [Imports](#imports)
    * [GUI](#gui)
    * [OneWire](#onewire)
    * [MultiPlot](#multiplot)
    * [RPiCamera](#rpicamera)
    * [RPiGPIO](#rpigpio)
  * [Setting up your IDE](#setting-up-your-ide)
  * [Remote programming using PC](#remote-programming-using-pc)
  * [Contact](#contact)

#Installation
## Setup RPi and install Coliform library
For instructions on how to setup RPi watch: [Getting started with NOOBS](https://youtu.be/-6OGuhLtKbU?t=684)

Before installing, you need to make sure you have pip installed, as it is required in order to install this module.
To install pip you can type the following into terminal:
```bash
curl -o https://bootstrap.pypa.io/get-pip.py
   
sudo python3 get-pip.py
```

Now to install the module:

In Raspberry Pi, or Linux Type the following into terminal:
```bash
sudo pip3 install Coliform
```
Or to upgrade an existing install:
```bash
sudo pip3 install -U Coliform
```

After installing Coliform, type this into terminal:
```python
python3
from Coliform import InitialSetup
InitialSetup.addShortcuts()
InitialSetup.installDependencies()
```

This will update your RPi and install all dependencies used in the Coliform package, it is recommended to install them this way because if they are installed from pip,
it would take a very long time to unpack sources and make the .whl packages required to install.

Be sure to answer all prompts during the install of the packages.

Additionally this command also adds all GUI application shortcuts to your desktop.

If you have a matplotlib error, try this:

Change matplotlib backend to TkAgg:

- Find out where the matplotlibrc file is so you can edit it. This can be done using the following in RPi Terminal:
  - ```python3```
  - ```import matplotlib```
  - ```matplotlib.matplotlib_fname()```
  - Take note of the address shown
  - ```exit()```
  - ```sudo nano /usr/local/lib/python3.4/dist-packages/mpl-data/matplotlibrc``` Note: if your address differs from this one, change it to your address.
  - Look for: ```backend: gtk3agg``` and change to: ```backend: Tkagg```
  - Press: ```Ctrl + X``` followed by ```y``` and ```ENTER``` or ```RETURN```

Now we need to enable Camera, 1-wire, SSH, and Remote GPIO:

From the Desktop:

* Click on Menu
* Preferences
* Raspberry Pi Configuration
* Interfaces
* Enable Camera, 1-wire, SSH, I2C, and Remote GPIO, then click OK

Note: In order to obtain temperature data from onewires, you need to complete some extra steps. These steps are shown in the [OneWire](#onewire) section of this document along with a schematic on how to connect to RPi.

#Requirements
* [pyserial](https://github.com/pyserial/pyserial) (only required if you need to use Arduino/ArduCAM)
* [Pillow](https://github.com/python-pillow/Pillow) (not required after version 0.5.3)
* [matplotlib](https://github.com/matplotlib/matplotlib)
* [picamera](https://github.com/waveform80/picamera) (not required after version 0.7.1)
* [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)
* [scipy](https://github.com/scipy/scipy) (required after version 0.7.0)
* [Adafruit_TCS34725](https://github.com/adafruit/Adafruit_Python_TCS34725) (required after version 0.7.3)

#Changelog
* Version 0.1
    - Initial Build 
* Version 0.1.1
    - Added install requirements to wheel package
* Version 0.2
    - Added MultiPlot and GPIO
    - Revamped OneWire and ArduCAM
    - Added PyPI Classifiers
* Version 0.2.1
    - Transferred Project GUI into Coliform module
* Version 0.2.2
    - Added GPL License classifiers.
* Version 0.3
    - Internal refactoring and cleaning up.
* Version 0.4
    - Merged Heater and Pump modules into a generic one called RPiGPIO
* Version 0.5
    - Added support for [picamera](https://github.com/waveform80/picamera), to use with our OV5647
    - Added corresponding GUI entries in order to get our results from OV5647
    - Began phasing out ArduCAM code
    - Added average intensity display to GUI
    - Added intensity to location plot.
    - General debugging for new camera features
    - Not Tested on RPi yet!
* Version 0.5.1
    - Stable tested release.
    - Fixed minor errors in previous beta version
    - Has minor GUI formatting errors.
* Version 0.5.2
    - Hotfix:
        - Fixed formatting errors found in previous version.
* Version 0.5.3
    - Fixed GUI formatting.
* Version 0.6
    - GUI and RPiCamera:
        - Changed intensity display range to 0-256
        - Fixed old formatting issues from OneWire module
        - Code restructuring for better fit good programming practices
        - Added image 'colorscaling' and functionality to various RPiCamera functions
        - Added more RPiCamera functions that better manage rgb data
* Version 0.6.1
    - Hotfix:
        - Fixed plots grid layout, and eliminated camera detection indicator because of critical error.
* Version 0.6.2
    - GUI:
        - Now Show Image and Show Plots display figures on different windows.
        - Fixed error display for when heater and pump are not conneted at pin 12 and 11 respectively.
* Version 0.6.3
    - Separated Camera GUI from the general GUI
    - Added support for changing camera options directly from Camera GUI or from command
* Version 0.6.4
    - Camera GUI:
        - Added Take Picture button
* Version 0.6.5
    - Hotfix:
        - Disabled exposure options until critical error is fixed.
* Version 0.6.6
    - Changed Camera GUI formatting
    - Added exposure modes
* Version 0.6.7
    - Fixed green scaling and increased camera speed.
* Version 0.6.8
    - Found and fixed critical GPIO error in RPiGPIO library.
* Version 0.6.9.1
    - Camera GUI and RPiCamera:
        - Added Brightness and Contrast options
* Version 0.6.9.3
    - Camera GUI and RPiCamera
    - Added framerate and shutterspeed options
* Version 0.7.0
    - Camera GUI and RPiCamera:
        - Added scipy as dependency
        - Added show image option for RBG components
        - Added standard option choices between low light and standard environment, for camera.
        - Added Auto White Balance options for camera
        - Added Save Image option
        - Added Save All option, which saves all images and plot
        - Added Zoom option, which allows delimitation to Region of Interest
        - Added and Import Image option, which allows import of existing image
        - Changed Image display from Show Image option, it now longer shows plot axis
        - Removed Take Picture Default option, now all pictures are taken with Take Picture option
      -  Added Camera Preview option
* Version 0.7.0.1
    - Removed scipy from setup.py dependencies, now it has to be manually installed before installing this package
* Version 0.7.1
    - Camera GUI, RPiCamera:
        - Changed protocol used to take pictures from picamera to raspistill because of green cast issues.
        - Found bug while testing, fails to take picture or show preview
* Version 0.7.1.1
    - Camera GUI, RPiCamera:
        - Fixed bug that prevented picture from being taken
        - Still can't show preview
* Version 0.7.1.2
    - Camera GUI, RPiCamera:
        - Fixed bug that prevented preview from being shown.
* Version 0.7.2
    - Camera GUI, RPiCamera:
        - Internal refactoring
        - changed shutter speed to microseconds
* Version 0.7.3
    - RGBSensor:
        - Added Adafruit TCS34725 RGB sensor support
    - GUI:
        - Added RGBSensor GUI
* Version 0.7.3.2
    - GUI:
        - Fixed GUI formatting error in RGBSensor GUI
* Version 0.7.4
    - GUI:
        - Changed backend from tkinter to qt5, using pyqt5
        - added pyqt5 to dependencies.
    - Created InitialSetup module, in order to ease the dependencies install process.
    - Removed most dependencies from pip packages, so they don't auto install, because they were causing problems.
* Version 0.7.4.1
    - Fixed error when installing dependencies.
* Version 0.7.4.2
    - Added more functionality to RPiCameraBackend, based on raspistill options.

#Usage
##Imports
Imports from module can be done as shown here:
```python
from Coliform import OneWire, Pump, ArduCAM, MultiPlot, Heater, RPiCamera
from Coliform import GUI
```
The first is for all functions, but the GUI, and the second is to import the GUI function.

##GUI
###Image Processing GUI
In order to display the project GUI, the following code can be used:
```python
from Coliform import GUI

GUI.startCameraGUI()
```
The GUI displayed should look like this:

[![Image_Processing_GUI](https://s15.postimg.org/lukk7d53v/image_processing_gui.png)](https://postimg.org/image/nmdj29ogn/)

####Description
Image parameters

- Resolution          : Set image resolution ```width``` x ```height```
- Delay               : Time (in s) before takes picture and shuts down (if not specified, set to 5s)
- Preview Timeout     : Same as Delay, but for preview.
- Contrast            : Set image contrast (-100 to 100)
- Brightness          : Set image brightness (0 to 100)
- ISO                 : Set capture ISO (100 to 800) (if set to 0, it will automatically try to choose best ISO for the environment.)
- Exposure            : Select exposure mode from those available. (default automatically tries to choose the best for the environment)
- Auto White Balance  : Select Auto Whte Balance from those available. (default automatically tires to choose the best for the environment)
- Zoom                : Set region of interest (x,y,width,height as normalised coordinates [0.0-1.0])
- Shutter Speed       : Set shutter speed in microseconds (if set to 0 it will automatically try to choose best shutter speed for the environment)

Camera Buttons

- Take Picture         : Captures image with selected parameters, saves rgb array and displays the intensity values in the Image Data section
- Set Normal Options   : Set normal environment values to image parameters.
- Set Low Light Options: Set Low Light environment values to image parameters.
- Camera Preview       : Starts preview of the capture using selected parameters for the duration stated at Preview Timeout box.
- Show Image           : Displays last captured image.
- Save Image           : Save last captured or imported image.
- Save All             : Saves image, plots, red, blue, and green components for last captured or imported image in a folder which name is the current selected image parameters 
- Show Plots           : Displays red, green, and blue image components and their corresponding histograms for last captured or imported image
- Import Image         : Imports selected image, saves rgb array and displays the intensity values in the Image Data section.
- Show Red             : Displays red component of last captured or imported image.
- Show Green           : Displays green component of last captured or imported image.
- Show Blue            : Displays blue component of last captured or imported image.

Image Data

- R                    : Red intensity value from last captured or imported image
- G                    : Green intensity value from last captured or imported image
- B                    : Blue intensity value from last captured or imported image
- I                    : Overall intensity value form last captured or imported image


###Control GUI
In order to display the project GUI, the following code can be used:
```python
from Coliform import GUI

GUI.startGUI()
```
The GUI displayed should look like this:

[![Control_GUI](https://s15.postimg.org/c8qzr2dy3/control_gui.png)](https://postimg.org/image/swihtk8pj/)

####Description

Temperature Sensor

- Temperature         : (in C) Displays temperature values for onewires connected.
- Show Plot           : Displays real-time temperature vs time plot for onewires connected.
- Save Data File      : Saves plot data to a csv file.

Heater

- Target Temperature  : Temperature to be maintained by the control loop.
- Heater ON           : Turns on Heater and begins control loop using temperature values obtained from the sensor.

Pump

- Power ON            : Starts pump PWM at 100 Hz
- Submit              : Changes pump PWM value to the one typed into the text box above. (0 to 100 Hz)

###RGB Sensor GUI
In order to display the project GUI, the following code can be used:
```python
from Coliform import GUI

GUI.startRGBSensorGUI()
```
The GUI displayed should look like this:

[![RGB_Sensor_GUI](https://s15.postimg.org/p2p1kerdn/rgb_sensor_gui.png)](https://postimg.org/image/w5wx00wt3/)

####Description

- Integration Time    : Select between available integration times, this is the time which the sensor remains open to integrate data.
- Gain                : Select between available gains, this multiplies data by selected gain value.

RGB Sensor Buttons

- Capture Data          : Captures sensor data and displays it in the RGB Data section
- Set Normal Options    : Set well lit environment integration and gain parameters.
- Set Low Light Options : Set low light integration and gain parameters.
- Save Data             : Saves data to text file.

##OneWire
###Setup
These group of functions allow you to detect one or multiple OneWires, get their address and display their respective temperature. This code was written and tested for [DS18B20](https://www.maximintegrated.com/en/products/analog/sensors-and-sensor-interface/DS18B20.html/tb_tab0) OneWires.

If multiple OneWires are connected, they need to be in the following configuration:
![OneWire Connection](https://camo.githubusercontent.com/99c16972ad946ec3d40c29d4999fdc90600728ac/68747470733a2f2f7570726d7265736561726368726573746f2e66696c65732e776f726470726573732e636f6d2f323031362f30392f6f6e657769726572706973657475702e706e673f773d34383326683d363431)

Where black, is ground, red is power (3.3V), and yellow is the digital signal. You also need a 4.7kΩ resistor connected as shown. All yellow (signal) cables send their signal to the GPIO4 pin of the RPi.

In order to detect OneWires, using the w1-gpio kernel driver, the GPIO4 pin has to be setup to recieve the information from them, in order to do this open the RPi terminal and do the following:

* Type: ```sudo nano /boot/config.txt```
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
```python
from Coliform import MultiPlot

MultiPlot.GeneratePlotDataFile(textfile, y_values, start_time)
MultiPlot.SaveToCsv(fileinput, fileoutput, filepath, y_amount)
MultiPlot.Plot(textfile, y_amount)

```
Sample Plot, using 3 OneWires:
[![tempplot.png](https://s22.postimg.org/b529vo7fl/tempplot.png)](https://postimg.org/image/5gvz4s331/)

##ArduCAM
```python
   from Coliform Import ArduCAM
   path = /home/
   filename = 'Test.jpg'
   portid = ArduCAM.getSerialPort()
   ArduCAM.TakePicture(path, portid[0], filename)
```

##RPiCamera
UPDATE IN PROGRESS...
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
from Coliform import RPiCamera

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

For further image processing and display, consider using [scipy](https://github.com/scipy/scipy), [numpy](https://github.com/numpy/numpy), and [matplotlib](https://github.com/matplotlib/matplotlib) python libraries, for image manipulation and display as described here:
  - [Advanced image processing using scipy and numpy](http://www.scipy-lectures.org/advanced/image_processing/)
  - [Image tutorial matplotlib](http://matplotlib.org/users/image_tutorial.html)

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

#Setting up your IDE
Download [Python 3](https://www.python.org/downloads/)

Important Note: When installing python 3, please click on Add to PATH, before continuing with install.

If you wish to install a python IDE on your computer, install PyCharm, for more information follow: 

* [Get PyCharm Pro](https://www.jetbrains.com/shop/eform/students) (For Students and Professors)
* [Getting Started with PyCharm](https://www.youtube.com/watch?v=BPC-bGdBSM8&list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP)

Learn Python: 

* [SoloLearn Python Course](https://www.sololearn.com/Course/Python/)
* [Python 3 Programming Introduction](https://pythonprogramming.net/introduction-to-python-programming/)
* [Non-Programmers Tutorial for Python 3](https://en.wikibooks.org/wiki/Non-Programmer%27s_Tutorial_for_Python_3)
* [List of Python Tutorials](http://docs.python-guide.org/en/latest/intro/learning/)
* [Official Python Tutorial](https://docs.python.org/3/tutorial/index.html)

#Remote Programming using PC
##Remote Desktop
RPi default login:
```bash
Username: pi
Password: raspberry
```

Connect Remotely to RPi desktop using Mac: [Remote connection to Raspberry Pi 3, Mac](https://www.youtube.com/watch?v=F_eUCMXhvgk)

Connect Remotely to RPi using Windows: [Connect wirelessly to Raspberry Pi](https://www.youtube.com/watch?v=toWBmUsWD6M)

Connect Remotely to RPi desktop using Windows: [Access Raspberry Pi Desktop (Windows)](https://www.youtube.com/watch?v=OE2FC1aSAqM)

##Using Pycharm (Harder)
This section is still in progress...

In order to run programs in the Raspberry Pi from your Windows, Linux, or Mac PC, you need to setup an ssh connection. You can do this with PyCharm IDE, following this: [Remote Programming of Raspberry Pi using PyCharm](http://www.codeproject.com/Tips/987276/Remote-Programming-of-RaspberryPi-using-PyCharm)

For Windows, download: [OpenSSH](https://www.mls-software.com/opensshd.html) and [MobaXterm](http://mobaxterm.mobatek.net/MobaXterm_Setup_9.3.msi), before setting up on PyCharm.

On Windows make sure to run MobaXterm and open an ssh connection, before opening Pycharm:

If you have any errors do the run the following on RPi terminal:

Check the config file in RPi:
```bash
sudo nano /etc/ssh/sshd-config
```
A line on the file should show:
```bash
X11Forwarding yes
```

Try to run a program again, if you still get an error:
Go to PyCharm > Run > Edit Configurations > Environment Variables, add:
```bash
Name        Value
DISPLAY     raspberrypi:10
```

If you still get errors, read additional [X11 Forwarding Debugging](http://www.seas.upenn.edu/cets/answers/x11-forwarding.html)

Additional information on setting up SSH: [Oracle Global Desktop Administration](https://docs.oracle.com/cd/E19351-01/821-1926/z40001c51312870.html#z40001c51375313)

