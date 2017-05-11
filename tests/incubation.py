from Coliform import RPiCameraBackend
from Coliform import OneWire
from Coliform import MultiPlot
import RPi.GPIO as GPIO
from time import sleep, time
import threading
import os

OneHourMilliseconds = 60*60*1000  # one hour in milliseconds
filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))  # set filepath to desktop
tf = 'PlotTextFile.txt'  # temporary plot text file
if os.path.isfile(tf):  # searches for preexisting temporary plot text file.
    os.remove(tf)  # destroys temporary plot text file, if it exists.


def takePicture():
    camera = RPiCameraBackend.PiCamera()  # camera initialization
    camera.resolution = (2952, 1944)  # image resolution
    camera.brightness = 50  # image brightness 0-100
    camera.contrast = 0  # image contrast 0-100
    camera.iso = 0  # camera iso 0-800
    camera.zoom = (0.0, 0.0, 1.0, 1.0)  # set image region of interest
    camera.timeout = 24*OneHourMilliseconds  # time for camera to shutdown in milliseconds
    camera.timelapse = OneHourMilliseconds  # time in between each image capture in milliseconds
    camera.quality = 75  # image quality 0-100, the higher the quality, less compression
    camera.exposure_mode = ''  # exposure mode set, default is auto
    camera.awb_mode = ''  # auto white balance set, default is auto
    camera.preview = (100, 100, 300, 200)  # set preview screen location and dimension
    camera.capture(mode='JPG', filename='image%04d.jpg')  # send capture function command to camera.

HeatSignalPin = 8  # pin that sends heat signal to arduino
LEDSignalPin = 10  # pin that sends led control signal to arduino
GPIO.setmode(GPIO.BOARD)  # sets GPIO in board mode, refers to pin number as board pin number in stead of GPIO number
GPIO.setup(HeatSignalPin, GPIO.OUT)  # sets heatsignalpin as out
GPIO.setup(LEDSignalPin, GPIO.OUT)  # sets ledsignalpin as out

captureThread = threading.Thread(target=takePicture)  # sets up new thread to run takePicture function
captureThread.start()  # start the thread that was setup in the previous line

start_time = time()  # save initial run time, for reference
elapsed_time = 0  # time elapsed since start_time value
i = 0  # hour counter
led_run_time_start = 0  # time counter for led run time
LEDStatus = 0  # led status indicator 0 = off, 1 = on

ids = OneWire.getOneWireID()  # Get IDs for connected onewires

while elapsed_time < (3600*24)+60:

    if elapsed_time >= i:
        GPIO.output(LEDSignalPin, GPIO.HIGH)  # sends LED on signal to arduino
        LEDStatus = 1  # sets LED status as ON
        i += 3600  # adds an hour for the next LED ON iteration
        led_run_time_start = elapsed_time  # sets current elapsed time as start for current LED run
    run_time = elapsed_time - led_run_time_start  # calculates run time from led start time

    if run_time > 5*60:
        if LEDStatus == 1:
            GPIO.output(LEDSignalPin, GPIO.LOW)  # after 5 minutes of ON time, if led is on, it is turned OFF
            LEDStatus = 0  # sets LED status to OFF

    TemperatureString, TemperatureFloat = OneWire.getTempList()
    MultiPlot.GeneratePlotDataFile(tf, TemperatureFloat, start_time)
    if elapsed_time == 0:
        y_title_axis = ['Temperature Plot', 'Temperature vs Time', 't(s)', 'T(C)', 'Sensor']  # plot title and axis labels
        MultiPlot.Plot(tf, len(ids), y_title_axis)  # start plot
    if TemperatureFloat[0] < 41.0:  # if temp is lower than 41 C
        GPIO.output(HeatSignalPin, GPIO.HIGH)  # sends high signal to heatsignalpin, which is sent to arduino. HIGH = 3.3V
    elif TemperatureFloat[0] >= 41.0:  # if temp is higher or equal to 41 C
        GPIO.output(HeatSignalPin, GPIO.LOW)  # sends low signal to heatsignalpin, which is sent to arduino. LOW = ~0V
    print(TemperatureString)  # print temperature values, for debugging purposes
    sleep(1)
    elapsed_time = int(time() - start_time)
GPIO.cleanup()  # cleans GPIO bus
tempfilename = 'TemperatureData.csv'  # sets filename for temperature data csv
y_variablename = 'TemperatureSensor'  # sets filenam for temperature sensor csv
MultiPlot.SaveToCsv(tf, tempfilename, filepath, len(ids), y_variablename)  # saves temperature data to csv file
