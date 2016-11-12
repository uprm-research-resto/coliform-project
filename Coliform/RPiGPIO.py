#!/usr/bin/env python3
#
# These are GPIO control functions for Coliform Module, based on RPi.GPIO module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import RPi.GPIO as GPIO

'''
import as:
from Coliform import RPiGPIO
use as:
VAR = RPiGPIO.Controller(pin,frequency)
VAR.startup()
VAR.HeaterPID()
VAR.SetIntensity()
VAR.shutdown()
'''


class Controller(object):
    def __init__(self, channel, frequency):
        self.channel = channel
        self.frequency = float(frequency)

    def startup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.OUT)
        self.pwm = GPIO.PWM(self.channel, self.frequency)
        self.pwm.start(self.frequency)

    def HeaterPID(self, targetvalue, currentvalue):
        if targetvalue > currentvalue:
            self.pwm.ChangeDutyCycle(100)
        elif targetvalue < currentvalue:
            self.pwm.ChangeDutyCycle(0)
        else:
            self.pwm.ChangeDutyCycle(0)

    def shutdown(self):
        self.pwm.stop()
        GPIO.cleanup()

    def setIntensity(self, freq):
        self.pwm.ChangeDutyCycle(float(freq))
