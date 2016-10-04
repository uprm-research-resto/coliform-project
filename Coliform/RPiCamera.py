#!/usr/bin/env python3
#
# This is the Camera feature function for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import time
import picamera
import picamera.array
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
from fractions import Fraction


def takePicture():
    with picamera.PiCamera() as camera:
        with picamera.array.PiYUVArray(camera) as stream:
            camera.resolution = (1024, 1008)
            time.sleep(2)
            camera.capture(stream, 'yuv')
            # print(stream.array.shape)
            # print(stream.rgb_array.shape)
            rgb_array = stream.rgb_array
            return rgb_array


def takePictureLow():
    with picamera.PiCamera(framerate=Fraction(1, 6)) as camera:
        with picamera.array.PiYUVArray(camera) as stream:
            camera.resolution = (1024, 1008)
            camera.shutter_speed = 6000000
            camera.iso = 800
            time.sleep(30)
            camera.exposure_mode = 'off'
            camera.capture(stream, 'yuv')
            # print(stream.array.shape)
            # print(stream.rgb_array.shape)
            rgb_array = stream.rgb_array
            return rgb_array


# noinspection PyTypeChecker
def returnIntensity(rgb_array):
    red_avg = np.mean((rgb_array[..., 0].flatten())*(100/255))
    green_avg = np.mean((rgb_array[..., 1].flatten())*(100/255))
    blue_avg = np.mean((rgb_array[..., 2].flatten())*(100/255))
    img_hsv = colors.rgb_to_hsv(rgb_array[..., :3])
    intensity_avg = np.mean((img_hsv[..., 2].flatten())*(100/255))
    return red_avg, green_avg, blue_avg, intensity_avg


def showImage(rgb_array):
    plt.imshow(rgb_array)
    plt.show()


def showPlot(rgb_array):
    img_hsv = colors.rgb_to_hsv(rgb_array[..., :3])
    lu1 = rgb_array[..., 0].flatten()
    plt.subplot2grid((2, 4), (0, 0))
    plt.plot(lu1, color='r', label='Red', linestyle='-')
    plt.title("Red by Location")
    plt.xlabel("Location")
    plt.ylabel("Value")
    plt.legend()

    lu2 = rgb_array[..., 1].flatten()
    plt.subplot2grid((2, 4), (0, 1))
    plt.plot(lu2, color='g', label='Green', linestyle='-')
    plt.title("Green by Location")
    plt.xlabel("Location")
    plt.ylabel("Value")
    plt.legend()

    lu3 = rgb_array[..., 2].flatten()
    plt.subplot2grid((2, 4), (0, 2))
    plt.plot(lu3, color='b', label='Blue', linestyle='-')
    plt.title("Blue by Location")
    plt.xlabel("Location")
    plt.ylabel("Value")
    plt.legend()

    lu4 = img_hsv[..., 2].flatten()
    plt.subplot2grid((2, 4), (0, 3))
    plt.plot(lu4, color='k', label='Intensity', linestyle='-')
    plt.title("Intensity by Location")
    plt.xlabel("Location")
    plt.ylabel("Value")
    plt.legend()

    lu5 = rgb_array[..., 0].flatten()
    plt.subplot2grid((2, 4), (1, 0))
    plt.hist(lu5, bins=256, range=(0, 256), histtype='stepfilled', color='r', label='Red')
    plt.title("Red")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu6 = rgb_array[..., 1].flatten()
    plt.subplot2grid((2, 4), (1, 1))
    plt.hist(lu6, bins=256, range=(0, 256), histtype='stepfilled', color='g', label='Green')
    plt.title("Green")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu7 = rgb_array[..., 2].flatten()
    plt.subplot2grid((2, 4), (1, 2))
    plt.hist(lu7, bins=256, range=(0, 256), histtype='stepfilled', color='b', label='Blue')
    plt.title("Blue")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    lu8 = img_hsv[..., 2].flatten()
    plt.subplot2grid((2, 4), (1, 3))
    plt.hist(lu8, bins=256, range=(0, 256), histtype='stepfilled', color='k', label='Intesity')
    plt.title("Intensity")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()

    # plt.hist((rgb_array).ravel(), bins=256, range=(0,1), fc = 'k', ec = 'k')
    plt.show()
