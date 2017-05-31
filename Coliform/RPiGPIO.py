#!/usr/bin/env python3
#
# These are GPIO control functions for Coliform Module, based on RPi.GPIO module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
# ATTENTION: there are some instabilities with this implementation, it is recommended you use the default RPi.GPIO interface
# this interface is imported as: import RPi.GPIO as GPIO
# more information of this interface can be found searching google for: RPi.GPIO
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

# this class works specifically for PWM control, NOT for ON - OFF
class Controller(object): # initializes controller class
    def __init__(self, channel, frequency):  # controller constructor with channel and frequency parameters
        self.channel = channel
        self.frequency = float(frequency)

    def startup(self):  # funciton that starts th GPIO board and pin required
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.channel, GPIO.OUT)
        self.pwm = GPIO.PWM(self.channel, self.frequency)
        self.pwm.start(self.frequency)

    def HeaterPID(self, targetvalue, currentvalue):  # runs heater control loop
        if targetvalue > currentvalue:
            self.pwm.ChangeDutyCycle(100)
        elif targetvalue < currentvalue:
            self.pwm.ChangeDutyCycle(0)
        else:
            self.pwm.ChangeDutyCycle(0)

    def shutdown(self):  # shuts down pins
        self.pwm.stop()
        GPIO.cleanup()

    def setIntensity(self, freq):  # modify frequency of the pin
        self.pwm.ChangeDutyCycle(float(freq))
