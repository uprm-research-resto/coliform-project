#!/usr/bin/env python3
#
# These are the main functions for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import serial
import os
import glob
import sys
import time
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
from shutil import copyfile
import RPi.GPIO as GPIO

class ArduCAM():
    def TakePicture(path, port, filename):
        try:
            ser = serial.Serial(port, 115200)
            target = open(os.path.join(path, filename), 'wb')
            d = ''
            next(ser)
            next(ser)
            ser.write(chr(16).encode())
            next(ser)
            next(ser)
            b = ser.read_until(b'\xff\xd9')
            target.write(b)
            for i in b:
                d+= hex(i)
            target.close()
        except AttributeError:
            pass

    def getSerialPort(*args):
        result = []
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/ttyACM[0-9]*')
        for port in ports:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        return result

class OneWire():
    def getTemp(id):
        try:
            mytemp = ''
            filename = 'w1_slave'
            f = open( id + '/' + filename, 'r')
            line = f.readline() # read 1st line
            crc = line.rsplit(' ',1)
            crc = crc[1].replace('\n', '')
            if crc=='YES':
                line = f.readline() # read 2nd line
                mytemp = line.rsplit('t=',1)
            else:
                mytemp = 99999
            f.close()
            return int(mytemp[1])
        except:
            return 99999

    def getOneWireID(*args):
        result = []
        ports = glob.glob('/sys/bus/w1/devices/28*')
        for port in ports:
            result.append(port)
        return result

    def SaveToCsv(fileinput,fileoutput,filepath,y_amount):
        if os.path.isfile(os.path.join(filepath,fileoutput)):
            os.remove(os.path.join(filepath,fileoutput))
        tempfile = 'UnformattedData.txt'
        copyfile(fileinput,tempfile)
        fi = open(os.path.join(filepath, fileoutput),'a+')
        fi.write('Time(s),')
        for i in range(0,y_amount):
            if i+1 != y_amount:
                fi.write('TemperatureSensor{}'.format(i+1)+',')
            else:
                fi.write('TemperatureSensor{}'.format(i+1)+'\n')
        fileData = open(tempfile,'r').read()
        dataList = fileData.split('\n')
        for eachLine in dataList:
            if len(eachLine) > 1:
                y_all, x = eachLine.split('-')
                out = x+','+y_all + '\n'
                fi.write(out)

    def getTempList(*args):
        temperature_raw = []
        temperaturesstr = []
        ids = OneWire.getOneWireID()
        for id in ids:
            tempvalue = '{:.3f}'.format(OneWire.getTemp(id)/float(1000))
            temperature_raw.append(tempvalue)
            temperaturesstr.append(tempvalue + ' C')
        temperature_degrees_string = '\n'.join(temperaturesstr)
        return (temperature_degrees_string, temperature_raw)

class Heater():
    def startHeater(pin, frequency):
        global HEATPWM
        GPIO.setmode(GPIO.BOARD)
        HEAT = pin
        GPIO.setup(HEAT,GPIO.OUT)
        HEATPWM = GPIO.PWM(HEAT, frequency)
        HEATPWM.start(frequency)

    def HeaterPID(targetvalue, currentvalue):
        if targetvalue > currentvalue:
            HEATPWM.ChangeDutyCycle(100)
        elif targetvalue < currentvalue:
            HEATPWM.ChangeDutyCycle(0)
        else:
            HEATPWM.ChangeDutyCycle(0)

    def stopHeater(*args):
        HEATPWM.stop()
        GPIO.cleanup()

class Pump():
    def startPump(pin, frequency):
        GPIO.setmode(GPIO.BOARD)
        PUMP = pin
        GPIO.setup(PUMP,GPIO.OUT)
        global PUMPPWM
        PUMPPWM = GPIO.PWM(PUMP, 100)
        PUMPPWM.start(float(frequency))

    def stopPump(*args):
        PUMPPWM.stop()
        GPIO.cleanup()

    def setPumpIntensity(frequency):
        PUMPPWM.ChangeDutyCycle(float(frequency))

class MultiPlot():
    def GeneratePlotDataFile(textfile, y_values, start_time):
        tf = textfile
        f = open(tf, 'a+')
        plottemp = ','.join(y_values)
        elapsed_time = str(int(time.time() - start_time))
        f.write(plottemp + '-' + elapsed_time + '\n')
        f.close()

    def Plot(textfile,y_amount):
        #Source File
        tf = textfile
        # Setup figure and subplots
        f = figure(num = 0, figsize = (12, 8))#, dpi = 100)
        f.suptitle("Temperature Plot", fontsize=12)
        a = subplot2grid((1, 1), (0, 0))

        # Set titles of subplots
        a.set_title('Temperature vs Time')

        # Turn on grids
        a.grid(True)

        # set label names
        a.set_xlabel("t(s)")
        a.set_ylabel("Temperature(C)")

        #set y limits
        a.set_ylim(0,50)

        #Data Placeholders
        dph = zeros(0)

        # set plots
        plots = {}
        lph1 = []
        lph2 = []
        for i in range(0,y_amount):
            plots['plt{}'.format(i)], = a.plot(dph,dph, label="Sensor{}".format(i+1))
            lph1.append(plots['plt{}'.format(i)])
            lph2.append(plots['plt{}'.format(i)].get_label())
            #set legends
        a.legend(lph1, lph2)

        #Setup animation function
        def updateData(self):
            pullData = open(tf,"r").read()
            dataList = pullData.split('\n')

            # Setup Lists
            xList = []
            for i in range(0,y_amount):
                plots['yList{}'.format(i)] = []

            for eachLine in dataList:
                if len(eachLine) > 1:
                    y_all, x = eachLine.split('-')
                    xList.append(int(x))
                    y = y_all.split(',')
                    for i in range(0,len(y)):
                        plots['yList{}'.format(i)].append(int(round(float(y[i]),0)))
            for i in range(0,y_amount):
                plots['plt{}'.format(i)].set_data(xList,plots['yList{}'.format(i)])
                plots['plt{}'.format(i)].axes.relim()
                plots['plt{}'.format(i)].axes.autoscale_view(True,True,True)
        ani = animation.FuncAnimation(f, updateData, interval=1000)
        plt.show()
