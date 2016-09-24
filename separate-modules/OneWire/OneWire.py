import os
import sys
import glob
from shutil import copyfile

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

def getOneWireID():
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

def getTempList():
    temperature_raw = []
    temperaturesstr = []
    ids = getOneWireID()
    for id in ids:
        tempvalue = '{:.3f}'.format(getTemp(id)/float(1000))
        temperature_raw.append(tempvalue)
        temperaturesstr.append(tempvalue + ' C')
    temperature_degrees_string = '\n'.join(temperaturesstr)
    return (temperature_degrees_string, temperature_raw)
