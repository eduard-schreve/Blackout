import pygame
import player
import battery
import backrounds
import maplib
from globals import *
import inventory

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)  # Create a resizable window with dimensions 1280x720
clock = pygame.time.Clock()
running = True

# player = player.player()  # Create an instance of the Player class

##KEY FLAGS
flag_e_pressed = False

# map.Exec_func_str("setb 19 collide False")
player = player.player()
battery = battery.Battery()
backrounds = backrounds.backrounds()
inventory = inventory.inventory()

custom_obj_functions = {
    "itemsConvert": inventory.Load_items_from_container
}

maps = ["Maps/tut1.tmx","Maps/1.tmx","Maps/2.tmx","Maps/3.tmx","Maps/4.tmx","Maps/5.tmx","Maps/6.tmx"]
map_index = 0
map = maplib.LevelControl(maps,screen,custom_obj_functions)
map.Load_map(map_index)

##set plr pos to spawn point
player.cords = [map.Get_obj("spwn").x,map.Get_obj("spwn").y]

player_cords = (player.cords[0], player.cords[1])  # Starting position of the player

container = False

pygame.mixer.music.load("ObservingTheStar.ogg")
pygame.mixer.music.play(-1) 
pygame.mixer.music.set_volume(0.5) # Volume from 0.0 to 1.0
 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_e:
                if container == False:
                    container = True
                else:
                    container = False

    #---MOVEMENT---#
    if backrounds.render_start_page(screen) == "start":  # Check if the left mouse button is pressed on the start page
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

        player_cords = player.Update(map)
        if map.Plr_exit((player_cords[0],player_cords[1],player.size[0],player.size[1])):  ##Load New level
            map_index +=1
            map.Load_map(map_index)
            player.cords = [map.Get_obj("spwn").x,map.Get_obj("spwn").y] #Set plr cords to spawn


        #---PLAYER INTERACT---#
        if pygame.key.get_pressed()[pygame.K_e] and not flag_e_pressed:  # Check if 'E' key is held down
            flag_e_pressed = True
            map.Interact((player_cords[0],player_cords[1],player.size[0],player.size[1]))
        elif not pygame.key.get_pressed()[pygame.K_e] and flag_e_pressed:
            flag_e_pressed = False

        ##DRAW
        screen.fill((0, 0, 0))  # Fill the screen with black color
        vis_distance = int(10*(battery.state/6000))
        map.Render_map((player_cords[0]+TILE_SIZE//2,player_cords[1]+TILE_SIZE//2),pygame.mouse.get_pos(),vis_distance)
        battery.render(screen)  # Render the battery on the screen
        player.render(screen)

        #---INVENTORY---#
        inventory.render(screen)
        if container:
            inventory.container(screen, True)  # Render the inventory container with items [0, 1, 2]
            inventory.switch_items()

    elif backrounds.render_start_page(screen) == "load":  # Check if the left mouse button is pressed on the start page
        chosen = backrounds.render_load(screen)  # Render the load screen if "load" is pressed
        print(chosen)

    elif backrounds.render_start_page(screen) == "quit":  # Check if the left mouse button is pressed on the start page
        running = False  # Exit the game loop if "quit" is pressed

    else:
        backrounds.render_start_page(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()