def runSensors():
    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)


    #second sensor
    TRIG = 27
    ECHO = 17

    print "Distance 2 Measurement In progress"

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    print "Waiting For Sensor 2 To Settle"
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    print "Distance 2:",distance,"cm"

    GPIO.cleanup()
