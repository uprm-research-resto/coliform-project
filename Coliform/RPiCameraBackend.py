#!/usr/bin/env python3
#
# This is raspistill frontend for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
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
        self.timeout = 5000  # milliseconds, The program will run for this length of time, then take the capture (if output is specified).
        self.timelapse = 0 # milliseconds, The specific value is the time between shots in milliseconds. Note you should specify %04d at the point in the filename where you want a frame count number to appear. Example: image%04d.jpg
        self.zoom = (0.0, 0.0, 1.0, 1.0)
        self.resolution = (2952, 1944) # image resolution (width, height)
        self.quality = 75 # jpeg compression indicator, where quality 100 is almost completely uncompressed
        self.preview = 'n' # preview settings: n = no preview, f = full screen preview. You can also choose to display preview at a specific location on the screen. This is done by typing 'x,y,w,h' where x and y are the location on screen and w and h are the height and width of the image.

    def capture(self, mode='JPG', filename='output.jpg'): # Note: remember, if you have a non zero timelapse, you have include %04d in filename. Example: image%04d.jpg
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

        if self.timeout != 5000:
            timeout = ' --timeout ' + str(self.timeout)
        else:
            timeout = ''

        if self.timelapse != 0:
            timelapse = ' --timelapse ' + str(self.timelapse)
            if '%04d' in filename:
                pass
            else:
                filename = 'image%04d.jpg'
        else:
            timelapse = ''

        if self.zoom != (0.0, 0.0, 1.0, 1.0):
            zoom = ' --roi ' + str(self.zoom).replace('(', '').replace(')', '').replace(' ', '')
        else:
            zoom = ''

        if self.resolution != (2952, 1944):
            resolution = ' --width ' + str(self.resolution[0]) + ' --height ' + str(self.resolution[1])
        else:
            resolution = ''

        if self.quality != 75:
            quality = ' --quality ' + str(self.quality)
        else:
            quality = ''

        if self.preview == 'n':
            preview = ' --nopreview'
        elif self.preview == 'f':
            preview = ''
        else:
            preview = '-p ' + str(self.preview)

        if mode in ['PNG', 'png']:
            encode = ' --encoding png'
            if '.jpg' in filename:
                filename = filename.replace('.jpg', '.png')

        elif mode in ['BMP', 'bmp']:
            encode = ' --encoding bmp'
            if '.jpg' in filename:
                filename = filename.replace('.jpg', '.bmp')

        elif mode in ['GIF', 'gif']:
            encode = ' --encoding gif'
            if '.jpg' in filename:
                filename = filename.replace('.jpg', '.gif')
        else:
            encode = ''

        os.system('raspistill --raw{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}'.format(preview, iso, brightness, contrast,
                                                                      shutterspeed, exposure, awb, timeout, timelapse, zoom,
                                                                      resolution, encode, quality, ' -o ', filename))
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
