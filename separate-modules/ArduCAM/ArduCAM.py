import serial
import os
import glob
import sys

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

def getSerialPort():
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
