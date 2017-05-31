#!/usr/bin/env python3
#
# These are OneWire functions for Coliform Module
#
# This file is part of Coliform. https://github.com/Regendor/coliform-project
# (C) 2016
# Author: Osvaldo E Duran
# Licensed under the GNU General Public License version 3.0 (GPL-3.0)
import glob  # used to locate ports and slave file of the onewire. In which onewire data is saved

'''
import as:
from Coliform import OneWire
use as:
To get temperature for all connected onewires:
TemperatureCelsius, TemperatureNoUnits = OneWire.getTempList()
Print values:
print(TemperatureCelsius)
Or:
print(TemperatureNoUnits)

To get onewire ids:
OneWire.getOneWireID()

'''


def getTemp(identifier):  # gets temperatuer value from selected one wire ID, where identifier is the specific one wire ID. This ID is obtained from getOneWireID function at line 38
    try:
        mytemp = ''  # empty temperature string variable
        filename = 'w1_slave'  # set slave filename that will be found and read
        f = open(identifier + '/' + filename, 'r')  # opens slave from the specific one wire ID as read only
        line = f.readline()  # read 1st line
        # Formatting in order to obtain crc signal, which states if a signal is found from the onewire
        crc = line.rsplit(' ', 1)
        crc = crc[1].replace('\n', '')
        if crc == 'YES':  # if yes, one wire with the specified ID is found
            line = f.readline()  # read 2nd line
            mytemp = line.rsplit('t=', 1)  # formatting in order to obtain temperature number
        else:
            mytemp = 99999  # sets to 99999 if onewire is not found
        f.close()  # close slave file
        return int(mytemp[1])  # returns temperature number
    except:
        return 99999  # sets to 99999 if slave file not found


def getOneWireID():  # gets ids of all connected one wires
    result = []  # empty list variable
    ports = glob.glob('/sys/bus/w1/devices/28*')  # locate all connected onewire addressees
    for port in ports:  # selects all addresses found and runs code inside loop for each one.
        result.append(port)  # adds each iteration of the ids found to the result list.
    return result  # returns result value, which is a list of all the ids found


def getTempList():  # gets temperature list of all connected one wires
    temperature_raw = []  # gets raw string values withoug the Celsius unit
    temperaturesstr = []  # gets string values with celsius unit
    ids = getOneWireID()  # gets one wire ids and saves to variable
    for identifier in ids: # for each id found, it will run the following code.
        tempvalue = '{:.3f}'.format(getTemp(identifier) / float(1000))  # runs getTemp function, found at line 19, formats the output and saves to variable
        temperature_raw.append(tempvalue)  # adds temperature for current id to raw temperature list
        temperaturesstr.append(tempvalue + ' C')  # adds temperature for current id with the Celsius unit to the string temperature list
    temperature_degrees_string = '\n'.join(temperaturesstr)  # formats temperature with units for better display in GUI
    return temperature_degrees_string, temperature_raw  # returns both values
