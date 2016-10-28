#!/usr/bin/env python3
#
# This is the main GUI function for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)

import os
from scipy import misc


class PiCamera(object):
    def __init__(self):
        self.iso = 0
        self.brightness = 50
        self.contrast = 0
        self.shutterspeed = 0  # microseconds
        self.exposure_mode = ''
        self.awb_mode = ''
        self.timeout = 5000  # milliseconds
        self.zoom = (0.0, 0.0, 1.0, 1.0)
        self.resolution = (2952, 1944)

    def capture(self, mode='JPG',filename='output.jpg'):
        if self.iso:
            iso = ' --ISO ' + str(self.iso)
        else:
            iso = ''

        if self.brightness != 50:
            brightness = ' --brightness ' + str(self.brightness)
        else:
            brightness = ''

        if self.contrast:
            contrast = ' --contrast ' + str(self.contrast)
        else:
            contrast = ''

        if self.shutterspeed:
            shutterspeed = ' --shutter ' + str(self.shutterspeed)
        else:
            shutterspeed = ''

        if self.exposure_mode:
            exposure = ' --exposure ' + self.exposure_mode
        else:
            exposure = ''

        if self.awb_mode:
            awb = ' --awb ' + self.awb_mode
        else:
            awb = ''

        if self.timeout != 5:
            timeout = ' --timeout ' + str(self.timeout)
        else:
            timeout = ''

        if self.zoom != (0.0, 0.0, 1.0, 1.0):
            zoom = ' --roi ' + str(self.zoom).replace('(', '').replace(')', '').replace(' ', '')
        else:
            zoom = ''

        if self.resolution != (2952, 1944):
            resolution = ' --width ' + str(self.resolution[0]) + ' --height ' + str(self.resolution[1])
        else:
            resolution = ''

        if mode in ['PNG', 'png']:
            encode = ' --encoding png'
            if filename == 'output.jpg':
                filename = 'output.png'

        elif mode in ['BMP', 'bmp']:
            encode = ' --encoding bmp'
            if filename == 'output.jpg':
                filename = 'output.bmp'

        elif mode in ['GIF', 'gif']:
            encode = ' --encoding gif'
            if filename == 'output.jpg':
                filename = 'output.gif'
        else:
            encode = ''

        os.system('raspistill --raw{}{}{}{}{}{}{}{}{}{}{}{}{}'.format(' --nopreview', iso, brightness, contrast,
                                                                      shutterspeed, exposure, awb, timeout, zoom,
                                                                      resolution, encode, ' -o ', filename))
        if mode in ['RGB', 'rgb']:
            rgb_array = misc.imread(filename)
            return rgb_array

    def preview(self):
        if self.iso:
            iso = ' --ISO ' + str(self.iso)
        else:
            iso = ''

        if self.brightness != 50:
            brightness = ' --brightness ' + str(self.brightness)
        else:
            brightness = ''

        if self.contrast:
            contrast = ' --contrast ' + str(self.contrast)
        else:
            contrast = ''

        if self.shutterspeed:
            shutterspeed = ' --shutter ' + str(self.shutterspeed)
        else:
            shutterspeed = ''

        if self.exposure_mode:
            exposure = ' --exposure ' + self.exposure_mode
        else:
            exposure = ''

        if self.awb_mode:
            awb = ' --awb ' + self.awb_mode
        else:
            awb = ''

        if self.timeout != 5:
            timeout = ' --timeout ' + str(self.timeout)
        else:
            timeout = ''

        if self.zoom != (0.0, 0.0, 1.0, 1.0):
            zoom = ' --roi ' + str(self.zoom).replace('(', '').replace(')', '').replace(' ', '')
        else:
            zoom = ''

        if self.resolution != (2952, 1944):
            resolution = ' --width ' + str(self.resolution[0]) + ' --height ' + str(self.resolution[1])
        else:
            resolution = ''

        os.system('raspistill --raw{}{}{}{}{}{}{}{}{}'.format(iso, brightness, contrast, shutterspeed,
                                                        exposure, awb, timeout, zoom, resolution))


