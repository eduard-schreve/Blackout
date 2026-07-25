import pygame
import random
import pathlib

pygame.init()

BASEDIR = pathlib.Path(__file__).parent

class backrounds:
    def __init__(self):
        self.start_page_image = pygame.image.load(BASEDIR.joinpath("Resources","start_page.png")).convert_alpha()  # Load the start page image
        self.buttons = pygame.image.load(BASEDIR.joinpath("Resources","buttons.png")).convert_alpha()  # Load the buttons image
        self.light = pygame.image.load(BASEDIR.joinpath("Resources","light.png")).convert_alpha()  # Load the light image
        self.load_screen = pygame.image.load(BASEDIR.joinpath("Resources","load_screen.png")).convert_alpha()  # Load the load screen image
        self.pressed = False  # Variable to track if the left mouse button is pressed

    def render_start_page(self, screen):
        self.start_page_image = pygame.transform.scale(self.start_page_image, (screen.get_width(), screen.get_height()))

        if pygame.mouse.get_pressed()[0]:
            mpos = pygame.mouse.get_pos()  # Get the current mouse position
            if pygame.Rect.collidepoint(pygame.Rect(100, 300, 256, 64), mpos):  # Check if the mouse is over the first button
                self.pressed = "start"  # Set pressed to "start" if the first button is clicked
            if pygame.Rect.collidepoint(pygame.Rect(100, 400, 256, 64), mpos):  # Check if the mouse is over the second button
                self.pressed = "load"  # Set pressed to "load" if the second button is clicked
            if pygame.Rect.collidepoint(pygame.Rect(100, 500, 256, 64), mpos):  # Check if the mouse is over the third button
                self.pressed = "quit"  # Set pressed to "quit" if the third button is clicked

        if not self.pressed:
            screen.blit(self.start_page_image, (0, 0))  # Render the start page image on the screen
            screen.blit(self.buttons, (100, 300), (0, 0, 256, 64))
            screen.blit(self.buttons, (100, 400), (0, 64, 256, 64))
            screen.blit(self.buttons, (100, 500), (0, 128, 256, 64))

            self.light.set_alpha(random.randint(0, 255))  # Set a random alpha value for the light image
            screen.blit(self.light, (screen.get_width() * 0.27578125, screen.get_height() * 0.0625))

        return self.pressed

    def render_load(self, screen):
        self.load_screen = pygame.transform.scale(self.load_screen, (screen.get_width(), screen.get_height()))
        screen.blit(self.load_screen, (0, 0))  # Render the load screen image on the screen