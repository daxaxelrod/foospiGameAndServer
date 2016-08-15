
def match_setup(cycle,enter,sound_player):
    # possible param -> new_player_btn
    
    import requests
    import RPi.GPIO as GPIO
    
    import time

    #works for any num players < 100
    players = requests.get("http://localhost:8000/api/v1/goals/").json()['results']    
    # if players.status_code != 200:
    #     print("Server not online")
    #asks for what players are playing
    asking = 2
    index = 0
    playing_players = []
    who_is_playing = {}

    # new_player_button = new_player_btn
    cycle_button = cycle
    enter_button = enter
    GPIO.setmode(GPIO.BCM)
    
    #pre cycle settup
    selected_player = players[index]
    sound_player.music.load("/home/pi/Documents/smartFoos/sensors/"+selected_player["path_to_sound_file"])
    sound_player.music.play()
    
    
    while asking:    
        if cycle_button.is_pressed:
            cycle_button.wait_for_release()
            #TODO what if they hold down both buttons
            
            if index < (len(players) - 1):
                index += 1
            else:
                index = 0
            selected_player = players[index]
            #play sound here
            print("{1}, Name {0}, sound {2}".format(selected_player['name'], index, selected_player['path_to_sound_file']))
            sound_player.music.load("/home/pi/Documents/smartFoos/sensors/"+selected_player["path_to_sound_file"])
            sound_player.music.play()

            #allow for pin to settle
            time.sleep(0.4)
               
        
        if enter_button.is_pressed:
            enter_button.wait_for_release()
            time.sleep(1)
            identical = False
            #first is red then blue
            print("Enter pressed")
            if len(playing_players) == 1:
                for player in playing_players:
                    if player['id']== selected_player['id']:
                        print("A person cannot play him/herself")
                        #maybe play an error noise here?
                        identical = True
                if not identical:
                    playing_players.append(selected_player)
                    asking -= 1
                    print("PLAY")
                    #confirmation sound
            else:
                playing_players.append(selected_player)
                asking -= 1
                print("Pick one more player!")
                # error sound
            
    who_is_playing = {
            "red_player": playing_players[0]['id'],
            "blue_player": playing_players[1]['id'] 
        }
    
    print("Who is playing")
    print(who_is_playing)
    
    return who_is_playing 
        

def match_gameplay(goal_wait,sound_player):
    import multiprocessing
    import RPi.GPIO as GPIO
    from datetime import datetime
    import time

    from goal_sensor import goal_sensor

    GPIO.setmode(GPIO.BCM)
    #red      #blue
    pins = [(23,24,1,"Red"),(27,17,2,"Blue")]

    # GPIO.cleanup()
    #making sure we don't get a false positive
    assurance_red = False
    assurance_blue = False
    post_goal_wait = goal_wait #seconds

    score = {
    "Red": 0,
    "Blue": 0
    }
    playing = True
    start_time = datetime.now()

    while playing:
        for pin in pins:
            goal = goal_sensor(pin)
            if goal:
                if pin[2]==1:
                    if assurance_red:
                        #GOOOAALALALALASO
                        print "GOAL RED"
                        score['Red'] += 1
                        assurance_red = False
                        time.sleep(post_goal_wait)
                    else:
                        print "assurance red true"
                        assurance_red = True
                if pin[2]==2:
                    if assurance_blue:
                        #GOAAAAALLLLLLLL
                        print "GOAL BLUE"
                        score['Blue'] += 1
                        assurance_blue = False
                        time.sleep(post_goal_wait)
                    else:
                        assurance_blue = True
                        print "assurance red true"
            #no goal for pin
            else:
                print "assurance false"
                if pin[2]==1:
                    assurance_red = False
                if pin[2]==2:
                    assurance_blue = False

            #winner
            print("testing")
            string_score = "{0}-{1}".format(score['Red'],score['Blue'])
            print string_score
            for (key,value) in score.iteritems():
                print "key: {0} value: {1}".format(key, value)
                if value >= 10:
                    print "there was a player that won"
                    sound_player.music.load("/home/pi/Documents/smartFoos/sensors/sounds/utils/{0}_won.mp3".format(key.lower()))
                    sound_player.music.play()
                    #there is another audio call right after this one
                    time.sleep(4)
                    print key + " Won"
                    playing = False
                    stop_time = datetime.now()
                    duration = stop_time - start_time
                    game_info = {
                        "winner": key,
                        "final_score":string_score,
                        "duration":round(duration.total_seconds(),3)
                        }
                    return game_info
