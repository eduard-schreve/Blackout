import pygame
import pathlib

pygame.init()

BASEDIR = pathlib.Path(__file__).parent

class player:
    def __init__(self):
        self.cords = [640, 360]  # Starting position
        self.speed = 3  # Speed of the player
        self.vel = [0,0]
        self.size = [25,25]
        self.position = 0  # Current position index for animation

        self.ogplayer_image = pygame.image.load(str(BASEDIR.joinpath("Resources","player.png"))).convert_alpha()  # Load the player image
        self.player_image = pygame.Surface((32, 32), pygame.SRCALPHA)  # Load the player image
        self.player_surface = pygame.Surface((32, 32), pygame.SRCALPHA)  # Create a surface for the player image
        self.player_image.blit(self.ogplayer_image, (0, 0), (0, 0, 32, 32))  # Blit the player image onto the surface

        self.angle = 0  # Angle of rotation for the player image

    def move_up(self):
        self.vel[1] -= self.speed
        self.angle = 0  # Set the angle to 0 when moving right
        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face right


    def move_down(self):
        self.vel[1] += self.speed
        self.angle = 180  # Set the angle to 180 when moving right
        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face right


    def move_left(self):
        self.vel[0] -= self.speed
        self.angle = 90  # Set the angle to 90 when moving right
        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face right


    def move_right(self):
        self.vel[0] += self.speed
        self.angle = -90  # Set the angle to -90 when moving right
        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)  # Rotate the player image to face right


    def doesnt_move(self):
        self.player_surface.fill((0, 0, 0, 0))  # Clear the player surface with transparency
        self.player_surface.blit(self.ogplayer_image, (0, 0), (0, 0, 32, 32))  # Blit the player image onto the surface
        self.player_image = pygame.transform.rotate(self.player_surface, self.angle)

    def Update(self,map):
        ##Update Pos
        new_x = self.cords[0]+self.vel[0]
        new_y = self.cords[1]+self.vel[1]
        collide_x = False
        collide_y = False
        collidors = map.Collisions((self.cords[0],self.cords[1],self.size[0],self.size[1]))
        for c in collidors:
            if pygame.rect.Rect(new_x,self.cords[1],self.size[0],self.size[1]).colliderect(c):
                collide_x = True
            if pygame.rect.Rect(self.cords[0],new_y,self.size[0],self.size[1]).colliderect(c):
                collide_y = True

        if not collide_x:
            self.cords[0] = new_x
        if not collide_y:
            self.cords[1] = new_y
        self.vel = [0,0]

        ##Update Animation
        if self.position < 16:
            self.position += 1
        else:
            self.position = 1

        return self.cords

    def render(self, screen):
        positions = [pygame.Rect(0, 0, 32, 32), #idle
                     pygame.Rect(32, 0, 32, 32), #walk1
                     pygame.Rect(32, 32, 32, 32), #walk2
                     pygame.Rect(32, 64, 32, 32), #walk3
                     pygame.Rect(32, 96, 32, 32),] #walk4

        # self.player_image = pygame.image.load("player.png").convert_alpha()  # Load the player image
        # self.player_surface.fill((0, 0, 0, 0))  # Clear the player surface with transparency
        # self.player_surface.blit(self.ogplayer_image, (0, 0), positions[self.position // 4])  # Blit the player image onto the surface
        screen.blit(self.player_image, (self.cords[0], self.cords[1]))  # Draw the player surface
        self.player_surface.fill((0, 0, 0, 0))  # Clear the player surface with transparency
        self.player_surface.blit(self.ogplayer_image, (0, 0), positions[self.position // 4])  # Blit the player image onto the surface