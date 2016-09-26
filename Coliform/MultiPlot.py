#!/usr/bin/env python3
#
# These are plot functions for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)

import time
from matplotlib.pylab import *
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.animation as animation
import os
from shutil import copyfile

'''
import as:
from Coliform import MultiPlot
use as:
MultiPlot.startGUI()
'''


def GeneratePlotDataFile(textfile, y_values, start_time):
    tf = textfile
    f = open(tf, 'a+')
    plottemp = ','.join(y_values)
    elapsed_time = str(int(time.time() - start_time))
    f.write(plottemp + '-' + elapsed_time + '\n')
    f.close()


def SaveToCsv(fileinput, fileoutput, filepath, y_amount):
    if os.path.isfile(os.path.join(filepath, fileoutput)):
        os.remove(os.path.join(filepath, fileoutput))
    tempfile = 'UnformattedData.txt'
    copyfile(fileinput, tempfile)
    fi = open(os.path.join(filepath, fileoutput), 'a+')
    fi.write('Time(s),')
    for i in range(0, y_amount):
        if i + 1 != y_amount:
            fi.write('TemperatureSensor{}'.format(i + 1) + ',')
        else:
            fi.write('TemperatureSensor{}'.format(i + 1) + '\n')
    fileData = open(tempfile, 'r').read()
    dataList = fileData.split('\n')
    for eachLine in dataList:
        if len(eachLine) > 1:
            y_all, x = eachLine.split('-')
            out = x + ',' + y_all + '\n'
            fi.write(out)
    fi.close()


def Plot(textfile, y_amount):
    # Source File
    tf = textfile
    # Setup figure and subplots
    f = figure(num=0, figsize=(12, 8))  # , dpi = 100)
    f.suptitle("Temperature Plot", fontsize=12)
    a = subplot2grid((1, 1), (0, 0))

    # Set titles of subplots
    a.set_title('Temperature vs Time')

    # Turn on grids
    a.grid(True)

    # set label names
    a.set_xlabel("t(s)")
    a.set_ylabel("Temperature(C)")

    # set y limits
    a.set_ylim(0, 50)

    # Data Placeholders
    dph = zeros(0)

    # set plots
    plots = {}
    lph1 = []
    lph2 = []
    for i in range(0, y_amount):
        plots['plt{}'.format(i)], = a.plot(dph, dph, label="Sensor{}".format(i + 1))
        lph1.append(plots['plt{}'.format(i)])
        lph2.append(plots['plt{}'.format(i)].get_label())
        # set legends
    a.legend(lph1, lph2)

    # Setup animation function
    def updateData(self):
        pullData = open(tf, "r").read()
        dataList = pullData.split('\n')

        # Setup Lists
        xList = []
        for i in range(0, y_amount):
            plots['yList{}'.format(i)] = []

        for eachLine in dataList:
            if len(eachLine) > 1:
                y_all, x = eachLine.split('-')
                xList.append(int(x))
                y = y_all.split(',')
                for i in range(0, len(y)):
                    plots['yList{}'.format(i)].append(int(round(float(y[i]), 0)))
        for i in range(0, y_amount):
            plots['plt{}'.format(i)].set_data(xList, plots['yList{}'.format(i)])
            plots['plt{}'.format(i)].axes.relim()
            plots['plt{}'.format(i)].axes.autoscale_view(True, True, True)

    ani = animation.FuncAnimation(f, updateData, interval=1000)
    plt.show()
