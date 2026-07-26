import pygame
import random
import pathlib

pygame.init()
pygame.mixer.init()

BASEDIR = pathlib.Path(__file__).parent

class backrounds:
    def __init__(self):
        self.start_page_image = pygame.image.load(BASEDIR.joinpath("Resources","start_page.png")).convert_alpha()  # Load the start page image
        self.buttons = pygame.image.load(BASEDIR.joinpath("Resources","buttons.png")).convert_alpha()  # Load the buttons image
        self.light = pygame.image.load(BASEDIR.joinpath("Resources","light.png")).convert_alpha()  # Load the light image
        self.load_screen = pygame.image.load(BASEDIR.joinpath("Resources","load_screen.png")).convert_alpha()  # Load the load screen image
        self.pressed = ""  # Variable to track if the left mouse button is pressed

    def render_start_page(self, screen):
        self.start_page_image = pygame.transform.scale(self.start_page_image, (screen.get_width(), screen.get_height()))

        click_sound = pygame.mixer.Sound("click.wav")
        click_sound.set_volume(1)

        # pygame.mixer.music.load("ObservingTheStar.ogg")
        # pygame.mixer.music.play(-1) 
        # pygame.mixer.music.set_volume(1) # Volume from 0.0 to 1.0

        if not self.pressed:
            screen.blit(self.start_page_image, (0, 0))  # Render the start page image on the screen

            self.light.set_alpha(random.randint(0, 255))  # Set a random alpha value for the light image
            screen.blit(self.light, (screen.get_width() * 0.27578125, screen.get_height() * 0.0625))

            mpos = pygame.mouse.get_pos()  # Get the current mouse position
            if pygame.Rect.collidepoint(pygame.Rect(100, 300, 256, 64), mpos):  # Check if the mouse is over the first button
                screen.blit(self.buttons, (100, 300), (0, 192, 256, 64))
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = "start"  # Set pressed to "start" if the first button is clicked
                    click_sound.play()
            else:
                screen.blit(self.buttons, (100, 300), (0, 0, 256, 64))

            if pygame.Rect.collidepoint(pygame.Rect(100, 400, 256, 64), mpos):  # Check if the mouse is over the second button
                screen.blit(self.buttons, (100, 400), (0, 256, 256, 64))
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = "load"  # Set pressed to "load" if the second button is clicked
                    click_sound.play()
            else:
                screen.blit(self.buttons, (100, 400), (0, 64, 256, 64))

            if pygame.Rect.collidepoint(pygame.Rect(100, 500, 256, 64), mpos):  # Check if the mouse is over the third button
                screen.blit(self.buttons, (100, 500), (0, 320, 256, 64))
                if pygame.mouse.get_pressed()[0]:
                    self.pressed = "quit"  # Set pressed to "quit" if the third button is clicked
                    click_sound.play()
            else:
                screen.blit(self.buttons, (100, 500), (0, 128, 256, 64))

        return self.pressed

    def render_load(self, screen):
        chosen = -1
        self.load_screen = pygame.transform.scale(self.load_screen, (screen.get_width(), screen.get_height()))
        screen.blit(self.load_screen, (0, 0))  # Render the load screen image on the screen

        levels = [pygame.Rect(50, 40, 200, 250),# 1
                  pygame.Rect(350, 40, 200, 250),# 2
                  pygame.Rect(650, 40, 200, 250),# 3
                  pygame.Rect(950, 40, 200, 250),# 4
                  pygame.Rect(50, 400, 200, 250),# 5
                  pygame.Rect(350, 400, 200, 250),# 6
                  pygame.Rect(650, 400, 200, 250),# 7
                  pygame.Rect(950, 400, 200, 250),# 8
                  ]       

        mpos = pygame.mouse.get_pos()
        for i in range(len(levels)):
            if pygame.Rect.collidepoint(levels[i], mpos):
                chosen = i

        return chosen