import pygame

# pygame setup
pygame.init()

image = pygame.image.load("battery.png")  # Load the battery image
imsurf = pygame.Surface(image.get_size(), pygame.SRCALPHA)  # Create a new surface with alpha channel

pygame.Surface.set_colorkey(image, (255, 255, 255))  # Set the color key to white for transparency
imsurf.blit(image, (0, 0))  # Blit the image onto the new surface

pygame.image.save(imsurf, "battery_transparent.png")  # Save the new surface as a transparent image