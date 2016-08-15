import requests
import pyglet
import time
from gpiozero import Button
import RPi.GPIO as GPIO
from pygame import mixer

from matchController import match_gameplay, match_setup
on = True
GPIO.setmode(GPIO.BCM)
cycle_button = Button(20)
enter_button = Button(16)
new_game_button = Button(21)
mixer.init()
time.sleep(1) #20 is normal

while on:
    print("Welcome to foosPi!")
    mixer.music.load("/home/pi/Documents/smartFoos/sensors/sounds/utils/lets_play.mp3")
    mixer.music.play()
    time.sleep(4)
    print "post play"
    #handle who is playing
    who_is_playing = match_setup(cycle_button, enter_button,sound_player=mixer) #maybe <-new_game_button
    #handles winner score and duration
    game_info = match_gameplay(.4,sound_player=mixer)
    # todo: handle epic goal
    
    
    #merges two dicts
    payload = who_is_playing.copy()
    payload.update(game_info)
    print(payload)
    response = requests.post("http://localhost:8000/api/v1/goals/games/", data = payload)
    print("response: {0}".format(response.status_code))
    print("press new button to play a new game. ")
    mixer.music.load("/home/pi/Documents/smartFoos/sensors/sounds/utils/play_again.mp3")
    mixer.music.play()

    timer = time.time()
    while True:
        seconds = time.time() - timer
        print(round(seconds,2))
        print new_game_button.value

        if 45 < seconds <= 46:
            mixer.music.load("/home/pi/Documents/smartFoos/sensors/sounds/utils/warning.mp3")
            mixer.music.play()
            print("WARNINGNGINGINGIGNIG")
            print("click the button or i turn off")
        if seconds >= 90:
            print("Thanks for playing!")
            print("Goodbye")
            mixer.music.load("/home/pi/Documents/smartFoos/sensors/sounds/utils/power_down.mp3")
            mixer.music.play()
            time.sleep(5)
            import os
            os.system("sudo shutdown -h now")
            
        time.sleep(0.1)
        # the pi is not perfect
        # if you poll then too often, you are going to get a false positive
        if new_game_button.is_pressed:
            on = True
            break

        
