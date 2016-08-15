def goal_sensor(gpio_pins):
    TRIG = gpio_pins[0]
    ECHO = gpio_pins[1]
    sensor_number = gpio_pins[2]

    import RPi.GPIO as GPIO
    import time
    GPIO.setmode(GPIO.BCM)


    # print "Distance {0} Measurement In progress".format(gpio_pins[3])

    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(0.1)

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

    print "Distance {0}: {1} cm".format(gpio_pins[3], distance)

    #returns true if there is a deviation from normal distance
    width_of_table = 60
    plus_or_minus = 15
    
    upper = width_of_table + plus_or_minus
    lower = width_of_table - plus_or_minus
    print lower,"<",distance,"<",upper
    if lower < distance:
        #no hand to grab ball
        return False
    else:
        #GOOOALALALALALAAASSOOOOO
        return True
