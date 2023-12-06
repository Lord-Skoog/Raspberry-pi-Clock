import time
import pygame
from pygame import mixer
from datetime import datetime
from pygame.locals import*
import RPi.GPIO as GPIO
import random
### SONG LIST
songlist = ['alarm.mp3', 'monkey.mp3', 'walnut.mp3']
### SONG LIST
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)
#if you're reading this the clock probably broke
#try updating all the imports and making sure the button is still hooked up correctly
#good luck if that doesn't work -Skoog
#Makes a digital clock in pygame


RES = WIDTH, HEIGHT = 1024, 600   #resoloution of raspi screen i used
pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

font = pygame.font.SysFont('TimesNewRoman', 200)

#if button press this function runs
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
#code for display clock
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
    clock.tick(20)
