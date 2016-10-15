#!/usr/bin/env python3
#
# This is the Camera feature function for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
from tkinter import filedialog
import time
import picamera
import picamera.array
import matplotlib.pyplot as plt
from scipy import misc
import matplotlib.colors as colors
import numpy as np
from fractions import Fraction
import os


def takePictureDefault(iso=100, brightness=50, contrast=0, resolution=(1024,1008)):
    with picamera.PiCamera() as camera:
        with picamera.array.PiYUVArray(camera) as stream:
            camera.resolution = resolution
            camera.brightness = brightness
            camera.contrast = contrast
            camera.iso = iso
            time.sleep(2)
            camera.capture(stream, 'yuv')
            # print(stream.array.shape)
            # print(stream.rgb_array.shape)
            rgb_array = stream.rgb_array
            return rgb_array


def takePicture(iso=100, delay=60, exposure='auto', resolution=(1024,1008), brightness=50, contrast=0, shutterspeed=0, framerate=25, zoom=(0.0, 0.0, 1.0, 1.0)):
    with picamera.PiCamera() as camera:
        with picamera.array.PiYUVArray(camera) as stream:
            camera.resolution = resolution
            camera.framerate = framerate
            camera.shutter_speed = shutterspeed
            camera.iso = iso
            camera.exposure_mode = exposure
            camera.brightness = brightness
            camera.contrast = contrast
            camera.zoom = zoom
            time.sleep(delay)
            camera.capture(stream, 'yuv')
            # print(stream.array.shape)
            # print(stream.rgb_array.shape)
            rgb_array = stream.rgb_array
            return rgb_array


def returnIntensity(rgb_array, color='all'):
    red_avg = np.mean(rgb_array[..., 0].flatten())
    green_avg = np.mean(rgb_array[..., 1].flatten())
    blue_avg = np.mean(rgb_array[..., 2].flatten())
    img_hsv = colors.rgb_to_hsv(rgb_array[..., :3])
    intensity_avg = np.mean(img_hsv[..., 2].flatten())
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


def importImage():
    image = filedialog.askopenfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
    rgb_array = misc.imread(image)
    return rgb_array


def saveImage(rgb_array):
    filename = filedialog.asksaveasfilename(filetypes=[('Image Files', '*.png *.jpg *.jpeg')])
    misc.imsave(filename, rgb_array)


def saveAllImages(rgb_array, foldername):
    directory = filedialog.askdirectory()
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
    misc.imsave(os.path.join(directory, foldername, trueimage), rgb_array)
    misc.imsave(os.path.join(directory, foldername, redimage), r_array)
    misc.imsave(os.path.join(directory, foldername, greenimage), g_array)
    misc.imsave(os.path.join(directory, foldername, blueimage), b_array)
    savePlot(rgb_array, os.path.join(directory, foldername, plotimage))


def startPreview(iso=100, timeout=10, exposure='auto', resolution=(1024,1008), brightness=50, contrast=0, shutterspeed=0, framerate=25, zoom=(0.0, 0.0, 1.0, 1.0)):
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.resolution = resolution
        camera.framerate = framerate
        camera.shutter_speed = shutterspeed
        camera.iso = iso
        camera.exposure_mode = exposure
        camera.brightness = brightness
        camera.contrast = contrast
        camera.zoom = zoom
        camera.start_preview()
        time.sleep(timeout)
        camera.stop_preview()


def showPlot(rgb_array):
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
