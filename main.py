import pygame
import player
import battery
import backrounds

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)  # Create a resizable window with dimensions 1280x720
clock = pygame.time.Clock()
running = True

player = player.player()  # Create an instance of the Player class
battery = battery.Battery()
backrounds = backrounds.backrounds()
##KEY FLAGS
flag_e_pressed = False


maps = ["Maps/Test_map.tmx","Maps/1.tmx"]
map = maplib.LevelControl(maps,screen)
map.Load_map(0)
# map.Exec_func_str("setb 19 collide False")
player = player.player()

##set plr pos to spawn point
player.cords = [map.Get_obj("spwn").x,map.Get_obj("spwn").y]

player_cords = (player.cords[0], player.cords[1])  # Starting position of the player

while running:

    screen.fill((255, 255, 255))  # Fill the screen with white color

    player.render(screen)  # Render the player on the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #---MOVEMENT---#
    if backrounds.render_start_page(screen) == "load":  # Check if the left mouse button is pressed on the start page
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

        battery.render(screen)  # Render the battery on the screen
    player_cords = player.Update(map)

    #---PLAYER INTERACT---#
    if pygame.key.get_pressed()[pygame.K_e] and not flag_e_pressed:  # Check if 'E' key is held down
        flag_e_pressed = True
        map.Interact((player_cords[0],player_cords[1],player.size[0],player.size[1]))
    elif not pygame.key.get_pressed()[pygame.K_e] and flag_e_pressed:
        flag_e_pressed = False

    ##DRAW
    screen.fill((0, 0, 0))  # Fill the screen with black color
    map.Render_map((player_cords[0]+TILE_SIZE//2,player_cords[1]+TILE_SIZE//2),pygame.mouse.get_pos(),player.torch_strength)

    if backrounds.render_start_page(screen) == "quit":  # Check if the left mouse button is pressed on the start page
        running = False  # Exit the game loop if "quit" is pressed

    pygame.display.flip()

    clock.tick(60)

pygame.quit()