import pygame
import player

pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

player = player.player()

player_cords = (player.cords[0], player.cords[1])  # Starting position of the player

while running:

    screen.fill((0, 0, 0))  # Fill the screen with black color

    player.render(screen)  # Render the player on the screen

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

    pygame.display.flip()

    clock.tick(60)

pygame.quit()