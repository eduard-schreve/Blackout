import math
import pygame

pygame.init()

class player:
    def __init__(self):
        self.cords = [640, 360]  # Starting position
        self.speed = 3  # Speed of the player
        self.position = 0  # Current position index for animation

        self.ogplayer_image = pygame.image.load("player.png").convert_alpha()  # Load the player image
        self.player_image = pygame.Surface((32, 32), pygame.SRCALPHA)  # Load the player image
        self.player_surface = pygame.Surface((32, 32), pygame.SRCALPHA)  # Create a surface for the player image
        self.player_image.blit(self.ogplayer_image, (0, 0), (0, 0, 32, 32))  # Blit the player image onto the surface

        self.angle = 0  # Angle of rotation for the player image

    def move_up(self):
        self.cords[1] -= self.speed  # Move up by decreasing the y-coordinate
        
        if self.position < 16:
            self.position += 1
        else:
            self.position = 1

        if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            mpos = pygame.mouse.get_pos()
            mvect = (mpos[0] - self.cords[0], mpos[1] - self.cords[1])  # Vector from player to mouse position
            self.angle = -math.degrees(math.atan2(mvect[1], mvect[0])) + -90  # Calculate the angle to the mouse position
        else:
            self.angle = 0  # Reset the angle to 0 when moving up

        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face left

        return self.cords

    def move_down(self):
        self.cords[1] += self.speed  # Move down by increasing the y-coordinate

        if self.position < 16:
            self.position += 1
        else:
            self.position = 1

        if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            mpos = pygame.mouse.get_pos()
            mvect = (mpos[0] - self.cords[0], mpos[1] - self.cords[1])  # Vector from player to mouse position
            self.angle = -math.degrees(math.atan2(mvect[1], mvect[0])) + -90  # Calculate the angle to the mouse position
        else:
            self.angle = 180  # Reset the angle to 0 when moving up

        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face left
        
        return self.cords

    def move_left(self):
        self.cords[0] -= self.speed  # Move left by decreasing the x-coordinate

        if self.position < 16:
            self.position += 1
        else:
            self.position = 1

        if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            mpos = pygame.mouse.get_pos()
            mvect = (mpos[0] - self.cords[0], mpos[1] - self.cords[1])  # Vector from player to mouse position
            self.angle = -math.degrees(math.atan2(mvect[1], mvect[0])) + -90  # Calculate the angle to the mouse position
        else:
            self.angle = 90  # Reset the angle to 0 when moving up

        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face left

        return self.cords

    def move_right(self):
        self.cords[0] += self.speed  # Move right by increasing the x-coordinate

        if self.position < 16:
            self.position += 1
        else:
            self.position = 1

        if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            mpos = pygame.mouse.get_pos()
            mvect = (mpos[0] - self.cords[0], mpos[1] - self.cords[1])  # Vector from player to mouse position
            self.angle = -math.degrees(math.atan2(mvect[1], mvect[0])) + -90  # Calculate the angle to the mouse position
        else:
            self.angle = -90  # Reset the angle to 0 when moving up

        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face right

        return self.cords

    def doesnt_move(self):
        if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
            mpos = pygame.mouse.get_pos()
            mvect = (mpos[0] - self.cords[0], mpos[1] - self.cords[1])  # Vector from player to mouse position
            self.angle = -math.degrees(math.atan2(mvect[1], mvect[0])) + -90  # Calculate the angle to the mouse position

        self.player_surface.fill((0, 0, 0, 0))  # Clear the player surface with transparency
        self.player_surface.blit(self.ogplayer_image, (0, 0), (0, 0, 32, 32))  # Blit the player image onto the surface
        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)

    def render(self, screen):
        positions = [pygame.Rect(0, 0, 32, 32), #idle
                     pygame.Rect(32, 0, 32, 32), #walk1
                     pygame.Rect(32, 32, 32, 32), #walk2
                     pygame.Rect(32, 64, 32, 32), #walk3
                     pygame.Rect(32, 96, 32, 32),] #walk4
        
        screen.blit(self.player_image, (self.cords[0], self.cords[1]))  # Draw the player surface
        self.player_surface.fill((0, 0, 0, 0))  # Clear the player surface with transparency
        self.player_surface.blit(self.ogplayer_image, (0, 0), positions[self.position // 4])  # Blit the player image onto the surface