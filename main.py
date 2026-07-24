import pygame
import maplib
import player
from globals import *

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

maps = ["Maps/Test_map.tmx"]
map = maplib.LevelControl(maps,screen)
map.load_map(0)

player = player.player()

##set plr pos to spawn point
player.cords = [11*32,11*32]

player_cords = (player.cords[0], player.cords[1])  # Starting position of the player

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #---MOVEMENT---#
    if pygame.key.get_pressed()[pygame.K_w]:  # Check if 'W' key is held down
        player_cords = player.move_up()  # Move the player up continuously while 'W' is held down

    elif pygame.key.get_pressed()[pygame.K_s]:  # Check if 'S' key is held down
        player_cords = player.move_down()  # Move the player down continuously while 'S' is held down

    elif pygame.key.get_pressed()[pygame.K_a]:  # Check if 'A' key is held down
        player_cords = player.move_left()  # Move the player left continuously while 'A' is held down

    elif pygame.key.get_pressed()[pygame.K_d]:  # Check if 'D' key is held down
        player_cords = player.move_right()  # Move the player right continuously while 'D' is held down
    else:
        player.doesnt_move()  # Reset the position index for animation when no movement keys are pressed

    ##DRAW
    screen.fill((0, 0, 0))  # Fill the screen with black color
    map.Render_map((player_cords[0]+TILE_SIZE//2,player_cords[1]+TILE_SIZE//2),pygame.mouse.get_pos())

    player.render(screen)  # Render the player on the screen

    pygame.display.flip()

    clock.tick(60)

pygame.quit()