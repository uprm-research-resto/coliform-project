# This is the RGB Sensor file of Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016 University of Puerto Rico Recinto Universitario de Mayaguez
#
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)

# Import the TCS34725 module.
import Adafruit_TCS34725
import os
from tkinter import filedialog
import time
import smbus


def Capture(integrationtime=2.4, gain=1, output='all'):
    try:
        # Dictionary for possible integration time values:
        dict = {}
        dict[2.4] = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_2_4MS  # (2.4ms, default)
        dict[24] = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_24MS
        dict[50] = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_50MS
        dict[101] = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_101MS
        dict[154] = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_154MS
        dict[700] = Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_700MS
        # Add possible gain values to Dictionary:
        dict[1] = Adafruit_TCS34725.TCS34725_GAIN_1X
        dict[4] = Adafruit_TCS34725.TCS34725_GAIN_4X
        dict[16] = Adafruit_TCS34725.TCS34725_GAIN_16X
        dict[60] = Adafruit_TCS34725.TCS34725_GAIN_60X

        # Create a TCS34725 instance with default integration time (2.4ms) and gain (4x).
        #tcs = Adafruit_TCS34725.TCS34725()

        # You can also override the I2C device address and/or bus with parameters:
        #tcs = Adafruit_TCS34725.TCS34725(address=0x30, busnum=2)

        # Or you can change the integration time and/or gain:

        tcs = Adafruit_TCS34725.TCS34725(integration_time=dict[integrationtime],
                                         gain=dict[gain])

        # Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
        tcs.set_interrupt(False)

        # Read the R, G, B, C color data.
        r, g, b, c = tcs.get_raw_data()

        # Calculate color temperature using utility functions.  You might also want to
        # check out the colormath library for much more complete/accurate color functions.
        color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)

        # Calculate lux with another utility function.
        lux = Adafruit_TCS34725.calculate_lux(r, g, b)

        if color_temp is None:
            raise AttributeError('Too dark to determine color temperature!')

        tcs.set_interrupt(True)
        tcs.disable()

        if output == 'all':
            return r, g, b, c, lux, color_temp
        elif output == 'rgbc':
            return r, g, b, c
        elif output == 'lux':
            return lux
        elif output == 'temp':
            return color_temp

    except KeyError:
        raise ValueError('No such integration time or gain, refer to coliform-project guide in github for possible options.')


def saveData(red=0, green=0, blue=0, clear=0, lux='0', colortemp='0'):
    filename = filedialog.asksaveasfilename(filetypes=[('Text File', '*.txt')])
    if os.path.isfile(filename):
        os.remove(filename)
    file = open(filename, 'a+')
    file.write(','.join(['Red: ' + str(red), 'Green: ' + str(green), 'Blue: ' + str(blue), 'Clear:' + str(clear),
                         'Luminosity: ' + lux, 'Color Temperature: ' + colortemp]))
    file.close()

    # Enable interrupts and put the chip back to low power sleep/disabled.

