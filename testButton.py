import RPi.GPIO as GPIO

try:
    from gpiozero import Button
    button = Button(21)
    b2 = Button(20)
    b3 = Button(16)
    while True:
        if button.is_pressed:
            print('1')
            button.wait_for_release()
            print("end of btn 1 press")
        if b2.is_pressed:
            print("2")
        if b3.is_pressed:
            print("3")
            
except Exception as e:
    print(type(e).__name__ + ": " + str(e))
    print("Cleaning up")
    GPIO.cleanup()

