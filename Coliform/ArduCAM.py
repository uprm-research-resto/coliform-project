#!/usr/bin/env python3
#
# These are camera for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
# This file contains frontend functions for arduino camera usage

# Imports:
import serial  # Serial package, used to recognize arducam through usb
import os  # os package used for file manipulation
import glob  # glob package used to search for arduino port
import sys  # sys package used to detect os and adapt to it

'''
import as:
from Coliform import GUI
use as:
GUI.startGUI()
'''


def TakePicture(path, port, filename):  # function used to take picture using arducam. path is the filepath where the image will be saved. filename is the image name. port is the port where the arduino es located, this is obtained with the getSerialPort function
    try:
        ser = serial.Serial(port, 115200)  # opens specified serial port
        target = open(os.path.join(path, filename), 'wb')  # creates file in which jpeg bytes from arduino are going to be written.
        d = ''
        next(ser)  # skips message that is not part of the image
        next(ser)  # skips message that is not part of the image
        ser.write(chr(16).encode())  # sends message that initiates image capture in arduino
        next(ser)  # skips message that is not part of the image
        next(ser)  # skips message that is not part of the image
        b = ser.read_until(b'\xff\xd9')  # reads output from arducam until jpeg exit flag
        target.write(b)  # writes jpeg data to file
        for i in b:  # save data as hex for debugging purposes
            d += hex(i)
        target.close()  # closes jpeg file
    except AttributeError:
        pass


def getSerialPort():  # function used to get arduino serial port
    result = []  # empty list variable created
    if sys.platform.startswith('win'):  # detects if platform is windows
        ports = ['COM' + str(i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):  # detects if platform is linux
        ports = glob.glob('/dev/ttyACM[0-9]*')
    for port in ports:  # saves all ports found
        s = serial.Serial(port)  # opens port
        s.close()  # closes port
        result.append(port)  # adds port to list
    return result  # returns list of ports
