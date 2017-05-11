import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)

GPIO.output(8,GPIO.HIGH)
GPIO.output(10,GPIO.HIGH)
sleep(10)
GPIO.output(8,GPIO.LOW)
GPIO.output(10,GPIO.LOW)
GPIO.cleanup()
