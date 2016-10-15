#!/usr/bin/env python3
#
# This is the main GUI function for Coliform Project
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import time
from Coliform import OneWire, MultiPlot, RPiGPIO, RPiCamera
from fractions import Fraction
from scipy import misc
from PIL import Image, ImageTk


# from datetime import datetime
'''
import as:
from Coliform import GUI
use as:
GUI.startGUI()
'''
# Defining global variables
PUMPPWM = None
HEATPWM = None
rgb_array = None
ids = []
TemperatureNumber = None


def startGUI():
    filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))
    # filename = 'TestJPEG.jpeg'
    tf = 'PlotTextFile.txt'
    if os.path.isfile(tf):
        os.remove(tf)

    def heaterpoweron():
        try:
            HeaterPowerStatus.set('Heater ON')
            heaterbutton.configure(text='Heater OFF')
            heaterbutton.configure(command=heaterpoweroff)
            global HEATPWM
            HEATPWM = RPiGPIO.Controller(12, 100)
            HEATPWM.startup()
            heaterbutton.after(1000, heaterinput)
        except (RuntimeError, AttributeError, NameError):
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
            messagebox.showinfo(message='Heater not detected on pin 12, please make sure its connected.')

    def heaterinput():
        try:
            if HeaterPowerStatus.get() != 'Heater OFF':
                value = float(temp.get())
                sensor = float(TemperatureNumber[1])
                HEATPWM.HeaterPID(value, sensor)
            heaterbutton.after(1000, heaterinput)
        except ValueError:
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
            messagebox.showinfo(message='Please type number into Target Temperature box.')
            heaterbutton.after(1000, heaterinput)

    def heaterpoweroff():
        try:
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
        except ValueError:
            pass

    def onewireon():
        try:
            global ids
            global TemperatureNumber
            ids = OneWire.getOneWireID()
            TemperatureDegrees, TemperatureNumber = OneWire.getTempList()
            templabel.config(text=TemperatureDegrees)
            MultiPlot.GeneratePlotDataFile(tf, TemperatureNumber, start_time)
            if not ids:
                TempSensorPowerStatus.set('Temp. Sensor OFF')
                templabel.config(text='NULL')
            else:
                TempSensorPowerStatus.set('Temp. Sensor ON')
            templabel.after(1000, onewireon)
        except IndexError:
            pass

    def tempplot():
        try:
            MultiPlot.Plot(tf, len(ids))
        except KeyError:
            messagebox.showinfo(message='No temperature sensor connected.')

    def savefile():
        tempfilename = 'TemperatureData.csv'
        MultiPlot.SaveToCsv(tf, tempfilename, filepath, len(ids))
        messagebox.showinfo(message='File saved to directory.')

    def pumppoweron():
        try:
            PumpPowerStatus.set("Pump ON")
            pumpbutton.configure(text='Pump OFF')
            pumpbutton.configure(command=pumppoweroff)
            global PUMPPWM
            PUMPPWM = RPiGPIO.Controller(11, 100)
            PUMPPWM.startup()

        except ValueError:
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            PUMPPWM.shutdown()
            messagebox.showinfo(message='Please type number from 0-100 into Pump text box.')

        except (RuntimeError, AttributeError, NameError):
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            messagebox.showinfo(message='Pump not detected, Please make sure pump is connected to pin 11')

    def pumppoweroff():
        try:
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            PUMPPWM.shutdown()

        except (AttributeError, RuntimeError):
            messagebox.showinfo(message='Please make sure pump is connected to pin 11.')

    def pumppowerchange():
        try:
            PUMPPWM.setIntensity(pumpintensity.get())
        except ValueError:
            messagebox.showinfo(message='Please type number from 0-100 into Pump text box.')

    def directorychosen():
        try:
            global filepath
            filepath = filedialog.askdirectory()
        except ValueError:
            pass

    root = Tk()
    root.title("Coliform Control GUI")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    temp = StringVar()
    PumpPowerStatus = StringVar()
    HeaterPowerStatus = StringVar()
    TempSensorPowerStatus = StringVar()
    pumpintensity = StringVar()

    HeaterPowerStatus.set('Heater OFF')
    PumpPowerStatus.set("Pump OFF")

    masterpane = ttk.Panedwindow(mainframe, orient=VERTICAL)

    toppane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)

    f2 = ttk.Labelframe(toppane, text='Temperature Sensor:', width=100, height=100)
    f3 = ttk.Labelframe(toppane, text='Heater:', width=100, height=100)
    toppane.add(f2)
    toppane.add(f3)
    masterpane.add(toppane)

    templabel = ttk.Label(f2)
    templabel.grid(column=1, row=2, sticky=W)
    ttk.Label(f2, text="Temperature:").grid(column=1, row=1, sticky=W)
    ttk.Button(f2, text='Show Plot', command=tempplot).grid(column=2, row=1, sticky=E)
    ttk.Button(f2, text='Save Data File', command=savefile).grid(column=2, row=2, sticky=(S, E))

    temp_entry = ttk.Entry(f3, width=7, textvariable=temp)
    temp_entry.grid(column=2, row=1, sticky=(W, E))
    ttk.Label(f3, text="Target Temperature:").grid(column=1, row=1, sticky=W)
    heaterbutton = ttk.Button(f3, text="Heater ON", command=heaterpoweron)
    heaterbutton.grid(column=1, row=2, sticky=W)

    bottompane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)
    f1 = ttk.Labelframe(bottompane, text='Status:', width=100, height=100)
    f4 = ttk.Labelframe(bottompane, text='Pump:', width=100, height=100)
    bottompane.add(f4)
    bottompane.add(f1)
    masterpane.add(bottompane)

    pumpbutton = ttk.Button(f4, text="Power ON", command=pumppoweron)
    pumpbutton.grid(column=1, row=1, sticky=W)
    pumpchangebutton = ttk.Button(f4, text="Submit", command=pumppowerchange)
    pumpchangebutton.grid(column=1, row=3, sticky=(W, E))
    pump_entry = ttk.Entry(f4, width=4, textvariable=pumpintensity)
    pump_entry.grid(column=1, row=2, sticky=(W, E))

    ttk.Label(f1, textvariable=TempSensorPowerStatus).grid(column=1, row=1, sticky=(W, E))
    ttk.Label(f1, textvariable=PumpPowerStatus).grid(column=1, row=2, sticky=(W, E))
    ttk.Label(f1, textvariable=HeaterPowerStatus).grid(column=1, row=3, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    temp_entry.focus()
    start_time = time.time()
    onewireon()
    heaterinput()
    root.mainloop()


def startCameraGUI():
    tf = 'PlotTextFile.txt'
    if os.path.isfile(tf):
        os.remove(tf)
    filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))

    def picturetaken():
        try:
            # global filename
            # filename = datetime.strftime(datetime.now(),"%Y.%m.%d-%H:%M:%S")+'.jpeg'
            iso = 100
            brightness = 50
            contrast = 0
            resolution = (2592,1944)
            global rgb_array
            if isovar.get():
                iso = isovar.get()
            if brightnessvar.get():
                brightness = brightnessvar.get()
            if contrastvar.get():
                contrast = contrastvar.get()
            if resolutionvarx.get() and resolutionvary.get():
                resolution = (resolutionvarx.get(),resolutionvary.get())
            rgb_array = RPiCamera.takePictureDefault(iso=iso, brightness=brightness, contrast=contrast, resolution=resolution)
            red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(rgb_array)
            intensity_array = '\n'.join(['R:'+'{:.3f}'.format(red_intensity),
                                         'G:'+'{:.3f}'.format(green_intensity),
                                         'B:'+'{:.3f}'.format(blue_intensity),
                                         'I:'+'{:.3f}'.format(intensity)])
            intensitylabel.config(text=intensity_array)

            # messagebox.showinfo(message='JPEG created on directory')
        except (UnboundLocalError, IndexError):
            # messagebox.showinfo(message='Arduino not found, make sure it is connected to USB port')
            pass

    def darkpicturetaken():
        try:
            # global filename
            # filename = datetime.strftime(datetime.now(),"%Y.%m.%d-%H:%M:%S")+'.jpeg'
            iso = 100
            resolution = (2592,1944)
            delay = 30
            brightness = 50
            contrast = 0
            shutterspeed = 0

            global rgb_array
            if isovar.get():
                iso = isovar.get()
            if delayvar.get():
                delay = delayvar.get()
            if resolutionvarx.get() and resolutionvary.get():
                resolution = (resolutionvarx.get(),resolutionvary.get())
            if brightnessvar.get():
                brightness = brightnessvar.get()
            if contrastvar.get():
                contrast = contrastvar.get()
            if shutterspeedvar.get():
                shutterspeed = shutterspeedvar.get() * 10**6
            if frameratevar.get():
                if '/' in frameratevar.get():
                    framelist = frameratevar.get().split('/')
                    if len(framelist) == 2:
                        framerate = Fraction(int(framelist[0]), int(framelist[1]))
                else:
                    framerate = int(frameratevar.get())
            rgb_array = RPiCamera.takePicture(iso=iso, delay=delay, resolution=resolution, exposure=exposuremode.get(),
                                              brightness=brightness, contrast=contrast, shutterspeed=shutterspeed,
                                              framerate=framerate)
            red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(rgb_array)
            intensity_array = '\n'.join(['R:'+'{:.3f}'.format(red_intensity),
                                         'G:'+'{:.3f}'.format(green_intensity),
                                         'B:'+'{:.3f}'.format(blue_intensity),
                                         'I:'+'{:.3f}'.format(intensity)])
            intensitylabel.config(text=intensity_array)

            # messagebox.showinfo(message='JPEG created on directory')
        except (UnboundLocalError, IndexError):
            # messagebox.showinfo(message='Arduino not found, make sure it is connected to USB port')
            pass

    def showimageplot():
        try:
            RPiCamera.showPlot(rgb_array)
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing plot.')

    def showimage():
        try:
            RPiCamera.showImage(rgb_array)
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')
        # except AttributeError:
        #     pass

    def showredimage():
        try:
            RPiCamera.showImage(rgb_array, 'r')
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')
        # except AttributeError:
        #     pass

    def showgreenimage():
        try:
            RPiCamera.showImage(rgb_array, 'g')
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')

    def showblueimage():
        try:
            RPiCamera.showImage(rgb_array, 'b')
        except ValueError:
            messagebox.showinfo(message='File not found, make sure take picture before showing Image.')

    # def directorychosen():
    #     try:
    #         global filepath
    #         filepath = filedialog.askdirectory()
    #     except ValueError:
    #         pass

    def importimage():
        global rgb_array
        rgb_array = RPiCamera.importImage()

        red_intensity, green_intensity, blue_intensity, intensity = RPiCamera.returnIntensity(rgb_array)
        intensity_array = '\n'.join(['R:' + '{:.3f}'.format(red_intensity),
                                     'G:' + '{:.3f}'.format(green_intensity),
                                     'B:' + '{:.3f}'.format(blue_intensity),
                                     'I:' + '{:.3f}'.format(intensity)])
        intensitylabel.config(text=intensity_array)

    def saveimage():
        RPiCamera.saveImage(rgb_array)

    def saveallimages():
        foldername = 'ISO:{}-Delay:{}-Resolution:{}x{}-Brightness:{}-Contrast:{}-Framerate:{}-ShutterSpeed:{}' \
                     '-Exposure:{}'.format(isovar.get(), delayvar.get(), resolutionvarx.get(), resolutionvary.get(),
                                           brightnessvar.get(), contrastvar.get(), frameratevar.get(),
                                           shutterspeedvar.get(), exposuremode.get())
        RPiCamera.saveAllImages(rgb_array, foldername)

    def preview():
        iso = 100
        resolution = (2592, 1944)
        brightness = 50
        contrast = 0
        shutterspeed = 0

        global rgb_array
        if isovar.get():
            iso = isovar.get()
        if previewtimeout.get():
            timeout = previewtimeout.get()
        if resolutionvarx.get() and resolutionvary.get():
            resolution = (resolutionvarx.get(), resolutionvary.get())
        if brightnessvar.get():
            brightness = brightnessvar.get()
        if contrastvar.get():
            contrast = contrastvar.get()
        if shutterspeedvar.get():
            shutterspeed = shutterspeedvar.get() * 10 ** 6
        if frameratevar.get():
            if '/' in frameratevar.get():
                framelist = frameratevar.get().split('/')
                if len(framelist) == 2:
                    framerate = Fraction(int(framelist[0]), int(framelist[1]))
            else:
                framerate = int(frameratevar.get())

        RPiCamera.startPreview(iso=iso, timeout=timeout, resolution=resolution, exposure=exposuremode.get(),
                               brightness=brightness, contrast=contrast, shutterspeed=shutterspeed,framerate=framerate)

    # def realtimeplot():
    #     MultiPlot.GeneratePlotDataFile(tf, RPiCamera.returnIntensity(rgb_array), start_time)

    root = Tk()
    root.title("Image Processing GUI")

    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    isovar = IntVar()
    resolutionvarx = IntVar()
    resolutionvary = IntVar()
    exposuremode = StringVar()
    delayvar = IntVar()
    contrastvar = IntVar()
    brightnessvar = IntVar()
    shutterspeedvar = IntVar()
    frameratevar = StringVar()
    previewtimeout = IntVar()

    exposuremode.set('off')
    shutterspeedvar.set(6)
    frameratevar.set('1/6')
    isovar.set(100)
    resolutionvary.set(1944)
    resolutionvarx.set(2592)
    delayvar.set(30)
    brightnessvar.set(50)
    previewtimeout.set(10)

    masterpane = ttk.Panedwindow(mainframe, orient=VERTICAL)

    midpane = ttk.Panedwindow(masterpane, orient=VERTICAL)
    f3 = ttk.Labelframe(midpane, text='More Options:',
                        width=100, height=100)
    f4 = ttk.Labelframe(midpane, text='Exposure Modes:', width=100, height=100)
    midpane.add(f3)
    midpane.add(f4)
    masterpane.add(midpane)

    ttk.Label(f3, text='Delay: ').grid(column=1, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=delayvar)
    delay_variable.grid(column=2, row=1, sticky=W)

    ttk.Label(f3, text='Brightness: ').grid(column=3, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=brightnessvar)
    delay_variable.grid(column=4, row=1, sticky=W)

    ttk.Label(f3, text='Contrast: ').grid(column=5, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=contrastvar)
    delay_variable.grid(column=6, row=1, sticky=W)

    ttk.Label(f3, text='Framerate: ').grid(column=7, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=frameratevar)
    delay_variable.grid(column=8, row=1, sticky=W)

    ttk.Label(f3, text='Shutter Speed: ').grid(column=9, row=1, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=shutterspeedvar)
    delay_variable.grid(column=10, row=1, sticky=W)

    ttk.Label(f3, text='ISO: (max=1600)').grid(column=1, row=2, sticky=E)
    iso_variable = ttk.Entry(f3, width=4, textvariable=isovar)
    iso_variable.grid(column=2, row=2, sticky=W)

    ttk.Label(f3, text='Resolution: (max=2592 x 1944)').grid(column=3, row=2, sticky=E)
    xresolution_variable = ttk.Entry(f3, width=4, textvariable=resolutionvarx)
    xresolution_variable.grid(column=4, row=2, sticky=E)
    ttk.Label(f3, text='x').grid(column=5, row=2)
    yresolution_variable = ttk.Entry(f3, width=4, textvariable=resolutionvary)
    yresolution_variable.grid(column=6, row=2, sticky=W)

    ttk.Label(f3, text='Preview Timeout: ').grid(column=7, row=2, sticky=E)
    delay_variable = ttk.Entry(f3, width=4, textvariable=shutterspeedvar)
    delay_variable.grid(column=8, row=2, sticky=W)

    exposuremode_night = ttk.Radiobutton(f4, text='night', variable=exposuremode, value='night')
    exposuremode_night.grid(column=1, row=1, sticky=W)

    exposuremode_backlight = ttk.Radiobutton(f4, text='auto', variable=exposuremode, value='auto')
    exposuremode_backlight.grid(column=2, row=1, sticky=W)

    exposuremode_verylong = ttk.Radiobutton(f4, text='verylong', variable=exposuremode, value='verylong')
    exposuremode_verylong.grid(column=3, row=1, sticky=W)

    exposuremode_spotlight = ttk.Radiobutton(f4, text='spotlight', variable=exposuremode, value='spotlight')
    exposuremode_spotlight.grid(column=4, row=1, sticky=W)

    exposuremode_sports = ttk.Radiobutton(f4, text='sports', variable=exposuremode, value='sports')
    exposuremode_sports.grid(column=5, row=1, sticky=W)

    exposuremode_off = ttk.Radiobutton(f4, text='off', variable=exposuremode, state=ACTIVE, value='off')
    exposuremode_off.grid(column=6, row=1, sticky=W)

    bottompane = ttk.Panedwindow(masterpane, orient=HORIZONTAL)
    f5 = ttk.Labelframe(bottompane, text='Camera Options:', width=100, height=100)
    f6 = ttk.Labelframe(bottompane, text='Image Data:', width=100, height=100)
    bottompane.add(f5)
    bottompane.add(f6)
    masterpane.add(bottompane)

    ttk.Button(f5, text='Take Picture Custom/Dark', command=darkpicturetaken).grid(column=1, row=1, sticky=(W, E))
    ttk.Button(f5, text="Take Picture Default", command=picturetaken).grid(column=1, row=2, sticky=(W, E))
    ttk.Button(f5, text="Camera Preview", command=preview).grid(column=1, row=3, sticky=(W, E))
    ttk.Button(f5, text="Save Image", command=saveimage).grid(column=1, row=4, sticky=(W, E))
    ttk.Button(f5, text="Show Plots", command=showimageplot).grid(column=2, row=2, sticky=(W, E))
    ttk.Button(f5, text="Show Image", command=showimage).grid(column=2, row=1, sticky=(W, E))
    ttk.Button(f5, text="Import Image", command=importimage).grid(column=2, row=3, sticky=(W, E))
    ttk.Button(f5, text="Save All", command=saveimage).grid(column=2, row=4, sticky=(W, E))
    ttk.Button(f5, text="Show Red", command=showredimage).grid(column=3, row=1, sticky=(W, E))
    ttk.Button(f5, text="Show Green", command=showgreenimage).grid(column=3, row=2, sticky=(W, E))
    ttk.Button(f5, text="Show Blue", command=showblueimage).grid(column=3, row=3, sticky=(W, E))

    ttk.Label(f6, text="Intensity: ").grid(column=1, row=1, sticky=(W, E))
    intensitylabel = ttk.Label(f6, text='Not Taken')
    intensitylabel.grid(column=1, row=2, sticky=(W, E))

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    start_time = time.time()
    root.mainloop()
