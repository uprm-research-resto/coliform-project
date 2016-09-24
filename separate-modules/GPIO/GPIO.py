import RPi.GPIO as GPIO

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

    def stopHeater():
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

    def stopPump():
        PUMPPWM.stop()
        GPIO.cleanup()

    def setPumpIntensity(frequency):
        PUMPPWM.ChangeDutyCycle(float(frequency))
