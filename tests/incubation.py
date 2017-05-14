from Coliform import RPiCameraBackend
from Coliform import RPiCamera
from Coliform import OneWire
from Coliform import MultiPlot
import RPi.GPIO as GPIO
from time import sleep, time
import threading
import os

OneHourMilliseconds = 60*60*1000  # one hour in milliseconds
filepath = os.sep.join((os.path.expanduser('~'), 'Desktop'))  # set filepath to desktop
tf = 'PlotTextFile.txt'  # temporary plot text file
itf = 'IntensityTextFile.txt'  # temporary plot file for intensity
if os.path.isfile(tf):  # searches for preexisting temporary plot text file.
    os.remove(tf)  # destroys temporary plot text file, if it exists.
if os.path.isfile(tf):  # searches for preexisting temporary plot text file.
    os.remove(tf)  # destroys temporary plot text file, if it exists.
ids = OneWire.getOneWireID()  # Get IDs for connected onewires


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


def startTemperaturePlot():
    y_title_axis = ['Temperature Plot', 'Temperature vs Time', 't(s)', 'T(C)', 'Sensor']  # plot title and axis labels
    MultiPlot.Plot(tf, len(ids), y_title_axis)  # start plot


def startIntensityPlot():
    y_title_axis = ['Light Intensity Plot', 'Intensity vs Time', 't(s)', 'I(RGB Value)', 'Color']  # plot title and axis labels
    MultiPlot.Plot(itf, 4, y_title_axis)  # start plot

HeatSignalPin = 8  # pin that sends heat signal to arduino
LEDSignalPin = 10  # pin that sends led control signal to arduino
GPIO.setmode(GPIO.BOARD)  # sets GPIO in board mode, refers to pin number as board pin number in stead of GPIO number
GPIO.setup(HeatSignalPin, GPIO.OUT)  # sets heatsignalpin as out
GPIO.setup(LEDSignalPin, GPIO.OUT)  # sets ledsignalpin as out

captureThread = threading.Thread(target=takePicture)  # sets up new thread to run takePicture function
captureThread.start()  # start the thread that was setup in the previous line

start_time = time()  # save initial run time, for reference
elapsed_time = 0  # time elapsed since start_time value
i = 0  # hour counter for led
j = 0  # image counter
k = 3650  # time counter for image loading and processing into array
led_run_time_start = 0  # time counter for led run time
LEDStatus = 0  # led status indicator 0 = off, 1 = on

while elapsed_time < (3600*24)+60:

    if elapsed_time >= i:
        GPIO.output(LEDSignalPin, GPIO.HIGH)  # sends LED on signal to arduino
        LEDStatus = 1  # sets LED status as ON
        i += 3540  # adds an hour for the next LED ON iteration
        led_run_time_start = elapsed_time  # sets current elapsed time as start for current LED run
    run_time = elapsed_time - led_run_time_start  # calculates run time from led start time
    if run_time > 4*60:
        if LEDStatus == 1:
            GPIO.output(LEDSignalPin, GPIO.LOW)  # after 5 minutes of ON time, if led is on, it is turned OFF
            LEDStatus = 0  # sets LED status to OFF

    if elapsed_time >= k:
        rgb_array = RPiCamera.importImage('image{:04d}.jpg'.format(j))  # imports previously taken image as rgb array
        red_avg, green_avg, blue_avg, intensity_avg = RPiCamera.returnIntensity(rgb_array)  # takes average values for rgb found in the array
        intensity_array = [red_avg, green_avg, blue_avg, intensity_avg]  # adds previous values to a list
        MultiPlot.GeneratePlotDataFile(itf, intensity_array, start_time)  # create image intensity data file
        j += 1  # adds to counter, to process next image
        k += 3600  # adds an hour to image counter, in order to wait for next image capture

    TemperatureString, TemperatureFloat = OneWire.getTempList()  # gets temperature values from onewires
    MultiPlot.GeneratePlotDataFile(tf, TemperatureFloat, start_time)  # create temperature plot data file
    if elapsed_time == 0:
        temperaturePlotThread = threading.Thread(target=startTemperaturePlot)  # sets up new thread to run startTemperaturePlot function
        temperaturePlotThread.start()  # start the thread that was setup in the previous line
    if elapsed_time >= 3651:
        intensityPlotThread = threading.Thread(target=startIntensityPlot)  # sets up new thread to run startTemperaturePlot function
        intensityPlotThread.start()  # start the thread that was setup in the previous line
    if float(TemperatureFloat[1]) < 41.0:  # if temp is lower than 41 C
        GPIO.output(HeatSignalPin, GPIO.HIGH)  # sends high signal to heatsignalpin, which is sent to arduino. HIGH = 3.3V
    elif float(TemperatureFloat[1]) >= 41.0:  # if temp is higher or equal to 41 C
        GPIO.output(HeatSignalPin, GPIO.LOW)  # sends low signal to heatsignalpin, which is sent to arduino. LOW = ~0V
    print(TemperatureString)  # print temperature values, for debugging purposes
    sleep(1)  # sets code to wait 1 second before running again
    elapsed_time = int(time() - start_time)  # calculates elapsed time from difference with start time
GPIO.cleanup()  # cleans GPIO bus
tempfilename = 'TemperatureData.csv'  # sets filename for temperature data csv
y_variablename = 'TemperatureSensor'  # sets variable name for temperature data csv
MultiPlot.SaveToCsv(tf, tempfilename, filepath, len(ids), y_variablename)  # saves temperature data to csv file

itempfilename = 'IntensityData.csv'  # sets file name for intensity data csv
iy_variablename = 'Intensity'  # sets variable name for intensity data csv
MultiPlot.SaveToCsv(itf, itempfilename, filepath, 4, iy_variablename)  # saves temperature data to csv file
