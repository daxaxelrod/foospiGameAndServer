import RPi.GPIO as GPIO
import time
import multiprocessing

def echo_time(pinNum):
    while GPIO.input(pinNum)==0:
        pulse_start = time.time()

    while GPIO.input(pinNum)==1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance, 2)
    print(distance)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

TRIG_1 = 23
ECHO_1 = 24

# second sensor
TRIG_2 = 27
ECHO_2 = 17

print "Distance 2 Measurement In progress"

GPIO.setup(TRIG_1,GPIO.OUT)
GPIO.setup(TRIG_2,GPIO.OUT)
GPIO.setup(ECHO_1,GPIO.IN)
GPIO.setup(ECHO_2,GPIO.IN)


GPIO.output(TRIG_1, False)
GPIO.output(TRIG_2, False)
print "Waiting For Sensor 2 To Settle"
time.sleep(2)

GPIO.output(TRIG_1, True)
GPIO.output(TRIG_2, True)
time.sleep(0.00001)
GPIO.output(TRIG_1, False)
GPIO.output(TRIG_2, False)

pins = [ECHO_1,ECHO_2]
for i in pins:
    p = multiprocessing.Process(target=echo_time(i))
    p.start()


