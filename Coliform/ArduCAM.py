#!/usr/bin/env python3
#
# These are camera for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import serial
import os
import glob
import sys

'''
import as:
from Coliform import GUI
use as:
GUI.startGUI()
'''


def TakePicture(path, port, filename):
    try:
        ser = serial.Serial(port, 115200)
        target = open(os.path.join(path, filename), 'wb')
        d = ''
        next(ser)
        next(ser)
        ser.write(chr(16).encode())
        next(ser)
        next(ser)
        b = ser.read_until(b'\xff\xd9')
        target.write(b)
        for i in b:
            d += hex(i)
        target.close()
    except AttributeError:
        pass


def getSerialPort():
    result = []
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/ttyACM[0-9]*')
    for port in ports:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    return result
