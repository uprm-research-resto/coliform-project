#!/usr/bin/env python3
#
# These are pump functions for Coliform Module
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


def startPump(pin, frequency):
    GPIO.setmode(GPIO.BOARD)
    PUMP = pin
    GPIO.setup(PUMP, GPIO.OUT)
    global PUMPPWM
    PUMPPWM = GPIO.PWM(PUMP, 100)
    PUMPPWM.start(float(frequency))


def stopPump():
    PUMPPWM.stop()
    GPIO.cleanup()


def setPumpIntensity(frequency):
    PUMPPWM.ChangeDutyCycle(float(frequency))
