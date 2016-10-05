#!/usr/bin/env python3
#
# These are OneWire functions for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
#
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import glob

'''
import as:
from Coliform import GUI
use as:
GUI.startGUI()
'''


def getTemp(identifier):
    try:
        mytemp = ''
        filename = 'w1_slave'
        f = open(identifier + '/' + filename, 'r')
        line = f.readline()  # read 1st line
        crc = line.rsplit(' ', 1)
        crc = crc[1].replace('\n', '')
        if crc == 'YES':
            line = f.readline()  # read 2nd line
            mytemp = line.rsplit('t=', 1)
        else:
            mytemp = 99999
        f.close()
        return int(mytemp[1])
    except:
        return 99999


def getOneWireID():
    result = []
    ports = glob.glob('/sys/bus/w1/devices/28*')
    for port in ports:
        result.append(port)
    return result


def getTempList():
    temperature_raw = []
    temperaturesstr = []
    ids = getOneWireID()
    for identifier in ids:
        tempvalue = '{:.3f}'.format(getTemp(identifier) / float(1000))
        temperature_raw.append(tempvalue)
        temperaturesstr.append(tempvalue + ' C')
    temperature_degrees_string = '\n'.join(temperaturesstr)
    return temperature_degrees_string, temperature_raw
