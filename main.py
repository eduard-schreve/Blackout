import pygame
import level_controller
from globals import *

##PYGAME SETUP
pygame.mixer.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN | pygame.RESIZABLE)
fps = 60
clock = pygame.time.Clock()

##MAP CONTROLLER STARTUP
map = level_controller.map(0,screen)

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()


    ##DRAW
    screen.fill('#000000')
    map.draw
    
