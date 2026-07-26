import pygame
import pathlib

pygame.init()

BASEDIR = pathlib.Path(__file__).parent

class inventory:
    def __init__(self):
        self.img = pygame.image.load(BASEDIR.joinpath("Resources","inventory.png")).convert_alpha()
        self.slots = [3, 4, 6]
        self.stash = [7, 7, 7]
        self.items = [pygame.Rect(0, 32, 32, 32), #red key 0
                      pygame.Rect(32, 32, 32, 32), #green key 1
                      pygame.Rect(64, 32, 32, 32), #blue key 2
                      pygame.Rect(0, 64, 32, 32), #red keycard 3
                      pygame.Rect(32, 64, 32, 32), #green keycard 4
                      pygame.Rect(64, 64, 32, 32), #blue keycard 5
                      pygame.Rect(0, 96, 32, 32), #battery 6
                      ]

    def render(self,screen):
        coords = [(screen.get_width() / 2 - 116, screen.get_height() - 100),
                  (screen.get_width() / 2 - 16, screen.get_height() - 100),
                  (screen.get_width() / 2 + 84, screen.get_height() - 100)]

        #---RENDER THE INVENTORY SLOTS---#
        screen.blit(self.img, coords[0], (0, 0, 32, 32))
        screen.blit(self.img, coords[1], (32, 0, 32, 32))
        screen.blit(self.img, coords[2], (64, 0, 32, 32))

        #---RENDER THE INVENTORY ITEMS---#
        for i in range(3):
            screen.blit(self.img, coords[i], self.items[self.slots[i]])

    def container(self, screen, in_range, items):
        coords = [(screen.get_width() - 250, screen.get_height() - 100),
                  (screen.get_width() - 150, screen.get_height() - 100),
                  (screen.get_width() -50, screen.get_height() - 100)]

        #---RENDER THE CONTAINER SLOTS---#
        if in_range:
            screen.blit(self.img, coords[0], (0, 0, 32, 32))
            screen.blit(self.img, coords[1], (32, 0, 32, 32))
            screen.blit(self.img, coords[2], (64, 0, 32, 32))

            font = pygame.font.SysFont("7 SEGMENTAL DIGITAL DISPLAY", 24)
            text_surf = font.render("CONTAINER:", True, (0, 255, 0))
            print(text_surf.get_size())
            screen.blit(text_surf, (screen.get_width() - 198, screen.get_height() - 130))

            #---RENDER THE INVENTORY ITEMS---#
            for i in range(3):
                screen.blit(self.img, coords[i], self.items[items[i]])


    def Load_items_from_container(self,strs:list[str]):
        items = []
        for str_item in strs:
            items.append(int(str_item))
        self.stash = [items[i] for i in range(len(items)) if i < 3]
