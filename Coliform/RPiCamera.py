#!/usr/bin/env python3
#
# This is the Camera feature function for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)


# Import:
# from Coliform import RPiCamera
# Usage:
# rgb_array1 = RPiCamera.takePicture() # takes picture with default parameters and returns rgb_array
# rgb_array2 = RPiCamera.takePicture(exposure='night', shutterspeed='6000000')  # takes picture with night exposure and 6 second shutter speed, all other values are default


# Imports:
import os
from Coliform import RPiCameraBackend
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
try:
    from scipy import misc
except ImportError:
    from tkinter import messagebox
    messagebox.showinfo(message='Please wait a 5-10 minutes while dependencies are installed.')
    os.system('sudo apt-get -y install python3-scipy')

# Function that takes pictures:


def takePicture(iso=0, exposure='', resolution=(2592, 1944), brightness=50, contrast=0, shutterspeed=0,
                timeout=5, zoom=(0.0, 0.0, 1.0, 1.0), awb_mode=''):
    """
    Takes image capture and returns rgb array

    :param iso: camera iso, values 0 to 800
    :param exposure: see exposure options
    :param resolution: max resolution (2592, 1944)
    :param brightness: image brightness, 0 to 100
    :param contrast: image contrast 0 to 100
    :param shutterspeed: image sutterspeed 0 to 6000000 ( in microseconds)
    :param timeout: in miliseconds
    :param zoom: selects region of interest. format: (0.0,0.0,1.0,1.0) where (x position, y position, relative lenght from xposition, relative length form y position). All values are normalized from 0.0 to 1.0
    :param awb_mode: see auto white balance options
    :return: returns rgb array

    Exposure options:
        '': uses default exposure mode
        auto: use automatic exposure mode
        night: select setting for night shooting
        nightpreview:
        backlight: select setting for backlit subject
        spotlight:
        sports: select setting for sports (fast shutter etc.)
        snow: select setting optimised for snowy scenery
        beach: select setting optimised for beach
        verylong: select setting for long exposures
        fixedfps: constrain fps to a fixed value
        antishake: antishake mode
        fireworks: select setting optimised for fireworks

    Auto White Balance Options:
        '': uses default auto white balance
        off: turn off white balance calculation
        auto: automatic mode (default)
        sun: sunny mode (between 5000K and 6500K)
        cloud: cloudy mode (between 6500K and 12000K)
        shade: shade mode
        tungsten: tungsten lighting mode (between 2500K and 3500K)
        fluorescent: fluorescent lighting mode (between 2500K and 4500K)
        incandescent: incandescent lighting mode
        flash: flash mode
        horizon: horizon mode
    """

    camera = RPiCameraBackend.PiCamera()
    camera.resolution = resolution  # max resolution (2592, 1944)
    camera.shutterspeed = shutterspeed # camera shutterspeed, in microseconds. the higher it is the longer exposure time to light
    camera.iso = iso  # camera iso (max 800)
    camera.exposure_mode = exposure # options given at line 17 through 30
    camera.brightness = brightness  # 0 - 100
    camera.contrast = contrast  # 0 - 100
    camera.awb_mode = awb_mode  # options given at line 32 to 33
    camera.zoom = zoom
    camera.timeout = timeout * 10**3  # convert to milliseconds
    rgb_array = camera.capture(mode='rgb')  # sets camera capture mode as rgb, as oposed to 'jpeg' or other file format and adds to variable

    return rgb_array  # returns rgb array


def returnIntensity(rgb_array, color='all'):
    """
    Returns average intensity for selected color values

    :param rgb_array: rgb array to be analyzed
    :param color: desired color outputs, see color options
    :return: returns desire color outputs

    Color Options:
    'a' or 'all': returns all colors
    'r' or 'red': returns red value only
    'g' or 'green': returns green value only
    'b' or 'blue': returns blue value only
    'rgb' or 'red, green, blue': returns red green blue values only
    'int' or 'intensity': returns overall intensity value only
    """

    red_avg = np.mean(rgb_array[..., 0].flatten())  # gets mean red intensity from array
    green_avg = np.mean(rgb_array[..., 1].flatten())  # gets mean green intensity from array
    blue_avg = np.mean(rgb_array[..., 2].flatten())  # gets mean blue intensity from array
    img_hsv = colors.rgb_to_hsv(rgb_array[..., :3])  # converts rgb array to hsv
    intensity_avg = np.mean(img_hsv[..., 2].flatten())  # get mean image intensity from hsv file

    # set all parameters that choose desired color output:
    if color in ['all', 'a']:
        return red_avg, green_avg, blue_avg, intensity_avg
    elif color in ['r', 'red']:
        return red_avg
    elif color in ['g', 'green']:
        return green_avg
    elif color in ['b', 'blue']:
        return blue_avg
    elif color in ['intensity', 'int']:
        return intensity_avg
    elif color in ['rgb', 'red, green, blue']:
        return red_avg, green_avg, blue_avg
    else:
        raise ValueError("Color parameter not recognized, please type one of the following: 'a', for all colors,"
                         " 'b' for blue, 'r' for red, 'g' for green, or 'int' for intensity")


def showImage(rgb_array, color='true'):
    """
    Displays image from array

    :param rgb_array: rgb array to be analyzed
    :param color: displays image with selected color filter. see color options

    Color options:
    'true' : displays image with no filter
    'r' : displays only red values from image
    'g' :  displays only green values from image
    'b' : displays only blue values from image
    """
    if color == 'true':
        f1 = plt.figure()
        f1.canvas.set_window_title('Image Capture')
        plt.imshow(rgb_array, interpolation='nearest')
        plt.axis('tight')
        plt.axis('off')
        # bbox_inches='tight'
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.show()
    if color == 'r':
        rgb_array_red = rgb_array * 1
        r_array = setImageColor(rgb_array_red, 'r')
        f2 = plt.figure()
        f2.canvas.set_window_title('Red Capture')
        plt.imshow(r_array, interpolation='nearest')
        plt.axis('tight')
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.show()
    if color == 'g':
        f3 = plt.figure()
        f3.canvas.set_window_title('Green Capture')
        rgb_array_green = rgb_array * 1
        g_array = setImageColor(rgb_array_green, 'g')
        plt.imshow(g_array, interpolation='nearest')
        plt.axis('tight')
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.show()
    if color == 'b':
        f4 = plt.figure()
        f4.canvas.set_window_title('Blue Capture')
        rgb_array_blue = rgb_array * 1
        b_array = setImageColor(rgb_array_blue, 'b')
        plt.imshow(b_array, interpolation='nearest')
        plt.axis('tight')
        plt.axis('off')
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.show()


def setImageColor(rgb_array, color):
    """
    Manually filter out colors not desired from an image rgb array.
    :param rgb_array: image array to be analyzed
    :param color: color to remain in array, see color options
    :return: returns image rgb array after filtering

    Color Options:
    'b': only keep blue color
    'r': only keep red color
    'g': only keep green color
    """
    if color in ['b', 'blue']:
        rgb_array[..., 0] *= 0
        rgb_array[..., 1] *= 0
    elif color in ['g', 'green']:
        rgb_array[..., 0] *= 0
        rgb_array[..., 2] *= 0
    elif color in ['r', 'red']:
        rgb_array[..., 1] *= 0
        rgb_array[..., 2] *= 0
    else:
        raise ValueError("Output color error: You need to specify which output you want from: 'r', 'g' or 'b'")
    return rgb_array


def importImage(imagepath):
    """
    Convert an image to array.

    :param imagepath: file path to image location. for example /pi/image.jpeg
    :return: returns image array
    """
    rgb_array = misc.imread(imagepath)
    return rgb_array


def saveImage(rgb_array, savepath):
    """
    Converts image array to file
    :param rgb_array: input rgb array
    :param savepath: save file location
    """
    misc.imsave(savepath, rgb_array)


def saveAllImages(rgb_array, directory, foldername):
    """
    Saves unfiltered and filtered images to a file directory
    :param rgb_array: image rgb array
    :param directory: image directory name
    :param foldername: name of the folder that will contain saved files
    :return:
    """
    rgb_array_red = rgb_array * 1
    r_array = setImageColor(rgb_array_red, 'r')
    rgb_array_green = rgb_array * 1
    g_array = setImageColor(rgb_array_green, 'g')
    rgb_array_blue = rgb_array * 1
    b_array = setImageColor(rgb_array_blue, 'b')
    trueimage = 'image.png'
    redimage = 'red.png'
    greenimage = 'green.png'
    blueimage = 'blue.png'
    plotimage = 'plot.png'
    if not os.path.exists(os.path.join(directory, foldername)):
        os.mkdir(os.path.join(directory, foldername))
    misc.imsave(os.path.join(directory, foldername, trueimage), rgb_array)
    misc.imsave(os.path.join(directory, foldername, redimage), r_array)
    misc.imsave(os.path.join(directory, foldername, greenimage), g_array)
    misc.imsave(os.path.join(directory, foldername, blueimage), b_array)
    savePlot(rgb_array, os.path.join(directory, foldername, plotimage))


def startPreview(iso=0, timeout=10, exposure='', resolution=(2592, 1944), brightness=50, contrast=0,
                 shutterspeed=0, zoom=(0.0, 0.0, 1.0, 1.0), awb_mode=''):
    camera = RPiCameraBackend.PiCamera()
    camera.resolution = resolution
    camera.shutterspeed = shutterspeed
    camera.iso = iso
    camera.exposure_mode = exposure
    camera.brightness = brightness
    camera.contrast = contrast
    camera.awb_mode = awb_mode
    camera.zoom = zoom
    camera.timeout = timeout * 10**3  # convert to milliseconds
    camera.preview()


def showPlot(rgb_array):
    """
    Shows rgb array plots for image
    :param rgb_array: rgb array to be analyzed
    """
    rgb_array_red = rgb_array * 1
    rgb_array_green = rgb_array * 1
    rgb_array_blue = rgb_array * 1
    rgb_array_hist = rgb_array

    f5 = plt.figure()
    f5.canvas.set_window_title('RGB Plots')

    lu1 = setImageColor(rgb_array_red, 'r')
    plt.subplot2grid((2, 3), (0, 0))
    plt.imshow(lu1)

    lu2 = setImageColor(rgb_array_green, 'g')
    plt.subplot2grid((2, 3), (0, 1))
    plt.imshow(lu2)

    lu3 = setImageColor(rgb_array_blue, 'b')
    plt.subplot2grid((2, 3), (0, 2))
    plt.imshow(lu3)

    lu4 = rgb_array_hist[..., 0].flatten()
    plt.subplot2grid((2, 3), (1, 0))
    plt.hist(lu4, bins=256, range=(0, 256), histtype='stepfilled', color='r', label='Red')
    plt.title("Red")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu5 = rgb_array_hist[..., 1].flatten()
    plt.subplot2grid((2, 3), (1, 1))
    plt.hist(lu5, bins=256, range=(0, 256), histtype='stepfilled', color='g', label='Green')
    plt.title("Green")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu6 = rgb_array_hist[..., 2].flatten()
    plt.subplot2grid((2, 3), (1, 2))
    plt.hist(lu6, bins=256, range=(0, 256), histtype='stepfilled', color='b', label='Blue')
    plt.title("Blue")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    # plt.hist((rgb_array).ravel(), bins=256, range=(0,1), fc = 'k', ec = 'k')
    plt.show()


def savePlot(rgb_array, filename):
    """
    Saves plot data for rgb array
    :param rgb_array: array to be analyzed
    :param filename: file path with filename to save the image. example /pi/plot.jpg
    """
    rgb_array_red = rgb_array * 1
    rgb_array_green = rgb_array * 1
    rgb_array_blue = rgb_array * 1
    rgb_array_hist = rgb_array

    f6 = plt.figure()
    f6.canvas.set_window_title('RGB Plots')

    lu1 = setImageColor(rgb_array_red, 'r')
    plt.subplot2grid((2, 3), (0, 0))
    plt.imshow(lu1)

    lu2 = setImageColor(rgb_array_green, 'g')
    plt.subplot2grid((2, 3), (0, 1))
    plt.imshow(lu2)

    lu3 = setImageColor(rgb_array_blue, 'b')
    plt.subplot2grid((2, 3), (0, 2))
    plt.imshow(lu3)

    lu4 = rgb_array_hist[..., 0].flatten()
    plt.subplot2grid((2, 3), (1, 0))
    plt.hist(lu4, bins=256, range=(0, 256), histtype='stepfilled', color='r', label='Red')
    plt.title("Red")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu5 = rgb_array_hist[..., 1].flatten()
    plt.subplot2grid((2, 3), (1, 1))
    plt.hist(lu5, bins=256, range=(0, 256), histtype='stepfilled', color='g', label='Green')
    plt.title("Green")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu6 = rgb_array_hist[..., 2].flatten()
    plt.subplot2grid((2, 3), (1, 2))
    plt.hist(lu6, bins=256, range=(0, 256), histtype='stepfilled', color='b', label='Blue')
    plt.title("Blue")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    # plt.hist((rgb_array).ravel(), bins=256, range=(0,1), fc = 'k', ec = 'k')
    f6.savefig(filename)
