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
        except (ValueError, RuntimeError, AttributeError):
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
            messagebox.showinfo(message='Heater not detected, make sure Heater is connected to pin 12')

    def heaterinput():
        try:
            if HeaterPowerStatus.get() != 'Heater OFF':
                value = float(temp.get())
                sensor = float(TemperatureNumber[1])
                HEATPWM.HeaterPID(value, sensor)
            heaterbutton.after(1000, heaterinput)
        except (RuntimeError, ValueError, AttributeError):
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
            messagebox.showinfo(message='Please type number into Target Temperature box. '
                                        'And make sure Heater is connected to pin 12')
            heaterbutton.after(1000, heaterinput)

    def heaterpoweroff():
        try:
            HEATPWM.shutdown()
            HeaterPowerStatus.set('Heater OFF')
            heaterbutton.configure(text='Heater ON')
            heaterbutton.configure(command=heaterpoweron)
        except (ValueError, AttributeError):
            messagebox.showinfo(message='Heater not detected on pin 12')

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

        except (RuntimeError, AttributeError, ValueError):
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            PUMPPWM.shutdown()
            messagebox.showinfo(message='Please type number from 0-100 into Pump text box.'
                                        ' And make sure pump is connected to pin 11')

    def pumppoweroff():
        try:
            PumpPowerStatus.set("Pump OFF")
            pumpbutton.configure(text='Pump ON')
            pumpbutton.configure(command=pumppoweron)
            PUMPPWM.shutdown()

        except (AttributeError, ValueError):
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

    def picturetaken():
        try:
            # global filename
            # filename = datetime.strftime(datetime.now(),"%Y.%m.%d-%H:%M:%S")+'.jpeg'
            global rgb_array
            rgb_array = RPiCamera.takePicture()
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
    f5 = ttk.Labelframe(bottompane, text='Camera Options:', width=100, height=100)
    f6 = ttk.LabelFrame(bottompane, text='Image Data:', width=100, height=100)
    bottompane.add(f4)
    bottompane.add(f5)
    bottompane.add(f6)
    bottompane.add(f1)
    masterpane.add(bottompane)

    pumpbutton = ttk.Button(f4, text="Power ON", command=pumppoweron)
    pumpbutton.grid(column=1, row=1, sticky=W)
    pumpchangebutton = ttk.Button(f4, text="Submit", command=pumppowerchange)
    pumpchangebutton.grid(column=1, row=3, sticky=(W, E))
    pump_entry = ttk.Entry(f4, width=4, textvariable=pumpintensity)
    pump_entry.grid(column=1, row=2, sticky=(W, E))

    ttk.Button(f5, text="Take Picture", command=picturetaken).grid(column=1, row=1, sticky=(W, E))
    ttk.Button(f5, text="Choose Directory", command=directorychosen).grid(column=1, row=4, sticky=(W, E))
    ttk.Button(f5, text="Show Plots", command=showimageplot).grid(column=1, row=2, sticky=(W, E))
    ttk.Button(f5, text="Show Image", command=showimage).grid(column=1, row=3, sticky=(W, E))

    ttk.Label(f6, text="Intensity: ").grid(column=1, row=1, sticky=(W, E))
    intensitylabel = ttk.Label(f6, text='Not Taken')
    intensitylabel.grid(column=1, row=2, sticky=(W, E))

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
