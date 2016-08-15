import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

# First Sensor
TRIG = 23
ECHO = 24

# second sensor
# TRIG = 27
# ECHO = 17

print "Distance 1 Measurement In progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "waiting For Sensor 1 To Settle"
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

print "Distance 1:",distance,"cm"

GPIO.cleanup()
