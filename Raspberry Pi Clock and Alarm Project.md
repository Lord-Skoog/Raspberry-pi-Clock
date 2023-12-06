For my final project of the semester I made a clock and alarm that displays using pygame. It uses a lot of imports, to explain I will go block by block of the code.
.........................................................
import time
import pygame
from pygame import mixer
from datetime import datetime
from pygame.locals import*
import RPi.GPIO as GPIO
import random

songlist = ['alarm.mp3', 'monkey.mp3', 'walnut.mp3']

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
.........................................................

this section of the code imports all of the functions needed for the program to run. We use time, datetime, and pygame for the clock portion.

We use mixer, gpio, and random in addition to the previous to run the alarm.

.........................................................

RES = WIDTH, HEIGHT = 1024, 600   #resoloution of raspi screen i used
pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

font = pygame.font.SysFont('TimesNewRoman', 200)

.........................................................

Above we start pygame, and set our font and text size that will display the time. 

.........................................................

def alarm():
    pygame.init()
    screen_size = (1024,600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("timer")
    time_left = 3 #duration of the timer in seconds
    crashed  = False
    font = pygame.font.SysFont("TimersNewRoman", 200)
    color = (255, 255, 255)

    while not crashed:
        for event in pygame.event.get():
            if event.type == QUIT:
                crashed = True
                exit()
        total_mins = time_left//60 # minutes left
        total_sec = time_left-(60*(total_mins)) #seconds left
        time_left -= 1
        if time_left > -1:
            text = font.render(("Time left: "+str(total_mins)+":"+str(total_sec)), True, color)
            screen.blit(text, (25, 50))
            pygame.display.flip()
            screen.fill((20,20,20))
            time.sleep(1)#making the time interval of the loop 1sec
        else:
            text = font.render("Break Over!!", True, color)
            screen.blit(text, (25, 50))
            pygame.display.flip()
            #code that picks a song from the songlist, can be as long as wanted, if you only
            #want 1 song then simply put 1 song in the list.
            g = len(songlist)
            a = random.randint(0, g)
            s = songlist[a]
            mixer.init()
            mixer.music.load(s)
            mixer.music.play()
            time.sleep(20)
            exit()
    return True

.........................................................

this is the alarm function. When a GPIO input is detected it starts the timer, currently the code is set to a 3 second timer. By chaging the value of 'time_left' we can lengthen that. You must put the desired amount of time in seconds. So 10 minutes would be a value of 600. The alarm will display them as minutes and not seconds until only 60 seconds remain. 

The 'else' if the if statement is triggered when we run out of time and the break ends. following that it will pick a random .mp3 file to play. It picks these from a list at the very beginning of the program clearly marked as 'SONGLIST'. as long as the mp3 files are in the same folder as the clock program. This is coded to cut the audio at 20 seconds, but you can adjust the length you want it to play for by edditing the final 'time.sleep' value. 

.........................................................

while True:
    if GPIO.input(21) != GPIO.HIGH:     #if button is pressed it stops the clock
        alarm()
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    surface.fill(pygame.Color('black'))

    t = datetime.now()  #current time

    time_render = font.render(f'{t:%r:%M:%S}', True, pygame.Color('white'), pygame.Color('black'))
    surface.blit(time_render, (1, 150)) #displays time in the device time setting
    #if device time is military it will display military.

    pygame.display.flip()
    clock.tick(20).........................................................

.........................................................

above is the final portion of the code, which is the clock code itself. value 't' is the current time, and then using pygame we display t in the same method as the device its running on. If it uses 24 hour time, so will the program, and so will 12 hour time. by default everything is black background and white font. This can be changed by editing 'pygame.Color' values. 

**CIRCUITS**

this program is meant to be run on a raspberry pi, and use a touchscreen display. It also utilizes GPIO and a button. A picture of how to wire it will be attached in the same repository as this. It is very simple. Wire Voltage to 5 or 3.3 volts, G to ground, and S to GPIO pin 21, or the top right corer of the GPIO pin cluster. 

