import pygame

pygame.init()

class Battery:
    def __init__(self):
        self.state = 6000  # Initialize the battery state to 100%

    def render(self, screen,):
        battery_image = pygame.image.load("battery.png").convert_alpha()  # Load the transparent battery image
        coords = (screen.get_width() - 74, 10)

        if self.state > -1:
            self.state -= 1
        else:
            self.state = 6000  # Reset the battery state to 100% when it reaches -1

        match self.state:
            case n if n > 4000:
                screen.blit(battery_image, coords, (0, 0, 64, 128))  # Render the battery with a high charge
            case n if n > 2000:
                # Render the battery with a medium charge
                screen.blit(battery_image, coords, (64, 0, 64, 128))  # Render the battery with a high charge
            case n if n > 1:
                # Render the battery with a low charge
                screen.blit(battery_image, coords, (128, 0, 64, 128))  # Render the battery with a high charge
            case 0:
                # Render the battery with an empty charge
                screen.blit(battery_image, coords, (192, 0, 64, 128))  # Render the battery with a high charge