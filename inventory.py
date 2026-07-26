import pygame

pygame.init()

class inventory:
    def __init__(self):
        self.img = pygame.image.load("inventory.png").convert_alpha()
        self.slots = [7, 7, 7]
        self.stash = [0, 1, 2]
        self.items = [pygame.Rect(0, 32, 32, 32), #red key 0
                      pygame.Rect(32, 32, 32, 32), #green key 1
                      pygame.Rect(64, 32, 32, 32), #blue key 2
                      pygame.Rect(0, 64, 32, 32), #red keycard 3
                      pygame.Rect(32, 64, 32, 32), #green keycard 4
                      pygame.Rect(64, 64, 32, 32), #blue keycard 5
                      pygame.Rect(0, 96, 32, 32), #battery 6
                      pygame.Rect(32, 96, 32, 32), #nothing 7
                      ]

        self.cont_selected = None
        self.inv_selected = None

    def render(self,screen): # inventory
        self.inv_coords = [(screen.get_width() / 2 - 116, screen.get_height() - 100),
                  (screen.get_width() / 2 - 16, screen.get_height() - 100),
                  (screen.get_width() / 2 + 84, screen.get_height() - 100)]

        #---RENDER THE INVENTORY SLOTS---#
        screen.blit(self.img, self.inv_coords[0], (0, 0, 32, 32))
        screen.blit(self.img, self.inv_coords[1], (32, 0, 32, 32))
        screen.blit(self.img, self.inv_coords[2], (64, 0, 32, 32))

        #---RENDER THE INVENTORY ITEMS---#
        for i in range(3):
            screen.blit(self.img, self.inv_coords[i], self.items[self.slots[i]])

            if self.inv_selected != None:
                screen.blit(self.img, (self.inv_coords[self.inv_selected]), pygame.Rect(64, 96, 32, 32))

    def container(self, screen, in_range):
        self.cont_coords = [(screen.get_width() - 250, screen.get_height() - 100),
                  (screen.get_width() - 150, screen.get_height() - 100),
                  (screen.get_width() -50, screen.get_height() - 100)]

        #---RENDER THE CONTAINER SLOTS---#
        if in_range:
            screen.blit(self.img, self.cont_coords[0], (0, 0, 32, 32))
            screen.blit(self.img, self.cont_coords[1], (32, 0, 32, 32))
            screen.blit(self.img, self.cont_coords[2], (64, 0, 32, 32))

            font = pygame.font.SysFont("7 SEGMENTAL DIGITAL DISPLAY", 24)
            text_surf = font.render("CONTAINER:", True, (0, 255, 0))
            screen.blit(text_surf, (screen.get_width() - 198, screen.get_height() - 130))

            #---RENDER THE CONTAINER ITEMS---#
            for i in range(3):
                screen.blit(self.img, self.cont_coords[i], self.items[self.stash[i]])

                if self.cont_selected != None:
                    screen.blit(self.img, (self.cont_coords[self.cont_selected]), pygame.Rect(64, 96, 32, 32))

            #---RENDER THE SELECTION CURSOR---#
            if pygame.mouse.get_pressed()[0]:
                mpos = pygame.mouse.get_pos()
                #---CONTAINER---#
                if pygame.Rect.collidepoint(pygame.Rect(self.cont_coords[0], (32, 32)), mpos):
                    screen.blit(self.img, (self.cont_coords[0]), pygame.Rect(64, 96, 32, 32))

                    if self.cont_selected != 0:
                        self.cont_selected = 0

                if pygame.Rect.collidepoint(pygame.Rect(self.cont_coords[1], (32, 32)), mpos):
                    screen.blit(self.img, (self.cont_coords[1]), pygame.Rect(64, 96, 32, 32))
                    
                    if self.cont_selected != 1:
                        self.cont_selected = 1

                if pygame.Rect.collidepoint(pygame.Rect(self.cont_coords[2], (32, 32)), mpos):
                    screen.blit(self.img, (self.cont_coords[2]), pygame.Rect(64, 96, 32, 32))
                    
                    if self.cont_selected != 2:
                        self.cont_selected = 2

                #---INVENTORY---#
                if pygame.Rect.collidepoint(pygame.Rect(self.inv_coords[0], (32, 32)), mpos):
                    screen.blit(self.img, (self.inv_coords[0]), pygame.Rect(64, 96, 32, 32))

                    if self.inv_selected != 0:
                        self.inv_selected = 0

                if pygame.Rect.collidepoint(pygame.Rect(self.inv_coords[1], (32, 32)), mpos):
                    screen.blit(self.img, (self.inv_coords[1]), pygame.Rect(64, 96, 32, 32))
                    
                    if self.inv_selected != 1:
                        self.inv_selected = 1

                if pygame.Rect.collidepoint(pygame.Rect(self.inv_coords[2], (32, 32)), mpos):
                    screen.blit(self.img, (self.inv_coords[2]), pygame.Rect(64, 96, 32, 32))
                    
                    if self.inv_selected != 2:
                        self.inv_selected = 2

            if pygame.mouse.get_pressed()[2]:
                self.inv_selected = None
                self.cont_selected = None

    def Load_items_from_container(self,strs:list[str]):
        items = []
        for str_item in strs:
            items.append(int(str_item))
        self.stash = [items[i] for i in range(len(items)) if i < 3]

    def switch_items(self):
        if self.inv_selected != None and self.cont_selected != None:
            temp = self.slots[self.inv_selected]
            self.slots[self.inv_selected] = self.stash[self.cont_selected]
            self.stash[self.cont_selected] = temp

            self.inv_selected = None
            self.cont_selected = None