#!/usr/bin/env python3
#
# These are heater functions for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import RPi.GPIO as GPIO

'''
import as:
from Coliform import GUI
use as:
GUI.startGUI()
'''


def startHeater(pin, frequency):
    GPIO.setmode(GPIO.BOARD)
    HEAT = pin
    GPIO.setup(HEAT, GPIO.OUT)
    global HEATPWM
    HEATPWM = GPIO.PWM(HEAT, frequency)
    HEATPWM.start(frequency)


def HeaterPID(targetvalue, currentvalue):
    if targetvalue > currentvalue:
        HEATPWM.ChangeDutyCycle(100)
    elif targetvalue < currentvalue:
        HEATPWM.ChangeDutyCycle(0)
    else:
        HEATPWM.ChangeDutyCycle(0)


def stopHeater():
    HEATPWM.stop()
    GPIO.cleanup()
