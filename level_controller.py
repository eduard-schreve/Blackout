import pytmx
from globals import *
import pygame
import pathlib

BASEDIR = pathlib.Path(__file__).parent

class map():
    def __init__(self, map_nom, scn):
        self.screen = scn
        self.all_maps = [str(BASEDIR.joinpath("Maps","Test_map.tmx"))]
        self.tmxdata = pytmx.load_pygame(self.all_maps[map_nom]) #map_nom is for which map to play
        #This is the pixel offset between the map origen(top-left) and the screen origen(0,0)
        self.offset_x = TILE_SIZE
        self.offset_y = TILE_SIZE
        #self.back_tint = self.tmxdata.get_layer_by_name("Background").tintcolor

        ##ANIMATION INDEX
        self.fire_index = 0
        self.conveyor_index = 0 
        self.diamond_index = 0
        self.cion_index = 0 
        self.counter = 0 #Frame counter

        ##INTERACT STUFF
        self.door_types = ["Red_door", "Green_door", "Blue_door"]
        self.lever_types = ["Red_lever", "Green_lever", "Blue_lever"]

        self.interact_list = []    #This will be a list of all the tiles on the interact layer
        self.animation_list = []   #This will be a list of all the tiles on the animations layer
        self.active_tile_list = [] #This will be a list of all the doors and other toggleable stuff
        self.platform_list = []    #This will be a list of all the tiles on the play_ground layer
        self.mid_ground_list = []  #This will be a list of all the tiles on the mid_ground layer
        self.danger_list = []      #This will be a list of all the tiles on the danger layer

        self.convert_map_to_list()

        ##EXIT
        # self.exit_obj = self.tmxdata.get_object_by_name("plr_Exit")
        # self.exit_obj_rect = pygame.Rect((self.exit_obj.x, self.exit_obj.y), (int(self.exit_obj.width), int(self.exit_obj.height)))
    

    def draw(self):
        for y in range (21):
            for x in range (31):
                tile_x = x+self.offset_x//TILE_SIZE
                tile_y = y+self.offset_y//TILE_SIZE
                ##BACKGROUND
                tile_image = self.tmxdata.get_tile_image(tile_x,
                                                         tile_y,
                                                         FLOOR)
                if tile_image != None:
                    ##If the Background tint clour isn't black then it gets a gray tint
                    ##If you dont want a tint clour make the tint colour Black(#000000)
                    self.screen.blit(tile_image, 
                                     (x*TILE_SIZE-(self.offset_x%TILE_SIZE), 
                                      y*TILE_SIZE-(self.offset_y%TILE_SIZE)))
                    tile_image.set_alpha(255)

        ##DANGER TILES           
        for t in self.danger_list:
            tile_image = self.tmxdata.get_tile_image_by_gid(t[2])
            self.screen.blit(tile_image, 
                            (t[0]*TILE_SIZE-self.offset_x, 
                             t[1]*TILE_SIZE-self.offset_y))

        ##PLATEFORMS            
        for t in self.platform_list:
            tile_image = self.tmxdata.get_tile_image_by_gid(t[2])
            self.screen.blit(tile_image, 
                            (t[0]*TILE_SIZE-self.offset_x, 
                             t[1]*TILE_SIZE-self.offset_y))

        ##MID_GROUND
        for t in self.mid_ground_list:
            tile_image = self.tmxdata.get_tile_image_by_gid(t[2])
            self.screen.blit(tile_image, 
                            (t[0]*TILE_SIZE-self.offset_x, 
                             t[1]*TILE_SIZE-self.offset_y))
                
        ##ANIMATED TILES
        for t in self.animation_list:
            tile_proprerties = self.tmxdata.get_tile_properties_by_gid(t[2]) #2 = index for gid   
            if tile_proprerties == None:
                continue  
                
            #Flames
            if tile_proprerties["type"] == "fire":
                if self.counter % tile_proprerties["frames"][self.fire_index].duration == 0:
                    self.fire_index = (self.fire_index+1)%len(tile_proprerties["frames"])
                tile_image = self.tmxdata.get_tile_image_by_gid(tile_proprerties["frames"][self.fire_index].gid)
        
                self.screen.blit(tile_image,
                                        (t[0]*TILE_SIZE-self.offset_x, 
                                        t[1]*TILE_SIZE-self.offset_y))
                
            #Conveyors
            if tile_proprerties["type"] == "Conveyor":
                if self.counter % tile_proprerties["frames"][self.conveyor_index].duration == 0:
                    self.conveyor_index = (self.conveyor_index+1)%len(tile_proprerties["frames"])
                tile_image = self.tmxdata.get_tile_image_by_gid(tile_proprerties["frames"][self.conveyor_index].gid)
        
                self.screen.blit(tile_image,
                                        (t[0]*TILE_SIZE-self.offset_x, 
                                        t[1]*TILE_SIZE-self.offset_y))
                        
        ##INTERACTIBLE ANIMATIONS - stuff like doors and levers
        for t in self.active_tile_list:
            tile_proprerties = self.tmxdata.get_tile_properties_by_gid(t[2])
            if tile_proprerties == None:
                continue 
            #Doors   - Might need to make changes because dont check what type it is
            if tile_proprerties["Open"]:
                interact_image = self.tmxdata.get_tile_image_by_gid(tile_proprerties["frames"][1].gid)
            else:
                interact_image = self.tmxdata.get_tile_image_by_gid(tile_proprerties["frames"][0].gid)

            self.screen.blit(interact_image,
                            (t[0]*TILE_SIZE-self.offset_x, 
                            t[1]*TILE_SIZE-self.offset_y))
                
        #Levers
        for t in self.interact_list:
            tile_proprerties = self.tmxdata.get_tile_properties_by_gid(t[2])
            if tile_proprerties == None:
                continue 
            if tile_proprerties["On"]:
                interact_image = self.tmxdata.get_tile_image_by_gid(tile_proprerties["frames"][1].gid)
            else:
                interact_image = self.tmxdata.get_tile_image_by_gid(tile_proprerties["frames"][0].gid)
            
            self.screen.blit(interact_image,
                            (t[0]*TILE_SIZE-self.offset_x, 
                            t[1]*TILE_SIZE-self.offset_y))
                
        self.counter += 1
               

    def Calculate_screen_pos(self, sprite_pos):
        ##Turns the map pos that is inserted to screen pos 
        return (sprite_pos[0]-self.offset_x, sprite_pos[1]-self.offset_y)
    

    def Check_Collisions(self, pos, rect):
        ##pos = (map_x, map_y)
        ##rect = (width, height)

        all_colide_corners = []

        ##Top Left
        TL = (int(pos[0]/TILE_SIZE), int((pos[1]+2)/TILE_SIZE)) #The +2 is just that it is a bit lower than 16
        ##Top Right
        TR = (int((pos[0]+rect[0])/TILE_SIZE), int((pos[1]+2)/TILE_SIZE))
        ##Bottom Left
        BL = (int(pos[0]/TILE_SIZE), int((pos[1]+rect[1])/TILE_SIZE))
        ##Bottom Right
        BR = (int((pos[0]+rect[0])/TILE_SIZE), int((pos[1]+rect[1])/TILE_SIZE))

        ##CHECK TOP LEFT CORNER
        tile = self.tmxdata.get_tile_image(TL[0], TL[1], STATIC_OBSTICLES)
        tile_prop = self.tmxdata.get_tile_properties(TL[0], TL[1], STATIC_OBSTICLES) #tile_prop = tile properties
        if tile != None:
            if tile_prop == None or not "Open" in tile_prop or not tile_prop["Open"]: #if the tile doesnt have the open propertie or the propertie is not true
                all_colide_corners.append("TL")

        ##CHECK TOP RIGHT CORNER
        tile = self.tmxdata.get_tile_image(TR[0], TR[1], STATIC_OBSTICLES)
        tile_prop = self.tmxdata.get_tile_properties(TR[0], TR[1], STATIC_OBSTICLES) #tile_prop = tile properties
        if tile != None:
            if tile_prop == None or not "Open" in tile_prop or not tile_prop["Open"]: #if the tile doesnt have the open propertie or the propertie is not true
                all_colide_corners.append("TR")
        
        ##CHECK BOTTOM LEFT CORNER
        tile = self.tmxdata.get_tile_image(BL[0], BL[1], STATIC_OBSTICLES)
        tile_prop = self.tmxdata.get_tile_properties(BL[0], BL[1], STATIC_OBSTICLES) #tile_prop = tile properties
        if tile != None:
            if tile_prop == None or not "Open" in tile_prop or not tile_prop["Open"]: #if the tile doesnt have the open propertie or the propertie is not true
                all_colide_corners.append("BL")

        ##CHECK BOTTOM RIGHT CORNER
        tile = self.tmxdata.get_tile_image(BR[0], BR[1], STATIC_OBSTICLES)
        tile_prop = self.tmxdata.get_tile_properties(BR[0], BR[1], STATIC_OBSTICLES) #tile_prop = tile properties
        if tile != None:
            if tile_prop == None or not "Open" in tile_prop or not tile_prop["Open"]: #if the tile doesnt have the open propertie or the propertie is not true
                all_colide_corners.append("BR")
        
        return all_colide_corners


    def Test_tile(self, map_layer, pos, rect):
        ##It will return the tile data of the tiles with which BL and BR collided
        ##pos = (x,y)
        ##rect = (width, height)
        collide_tiles = []
        ##Top Left
        TL = (int(pos[0]/TILE_SIZE), int((pos[1]+2)/TILE_SIZE)) #The +2 is just that it is a bit lower than 16
        ##Top Right
        TR = (int((pos[0]+rect[0])/TILE_SIZE), int((pos[1]+2)/TILE_SIZE))
        ##Bottom Left
        BL = (int(pos[0]/TILE_SIZE), int((pos[1]+rect[1]/2)/TILE_SIZE))
        ##Bottom Right
        BR = (int((pos[0]+rect[0])/TILE_SIZE), int((pos[1]+rect[1]/2)/TILE_SIZE))

        tile = self.tmxdata.get_tile_properties(BL[0], BL[1], map_layer)
        if tile != None:
            collide_tiles.append(tile)

        tile = self.tmxdata.get_tile_properties(BR[0], BR[1], map_layer)
        if tile != None:
            collide_tiles.append(tile)

        tile = self.tmxdata.get_tile_properties(TL[0], TL[1], map_layer)
        if tile != None:
            collide_tiles.append(tile)

        tile = self.tmxdata.get_tile_properties(TR[0], TR[1], map_layer)
        if tile != None:
            collide_tiles.append(tile)

        return collide_tiles
    

    def tile_interact(self,pos):
        ##pos == map_pos
        tile = self.tmxdata.get_tile_properties(pos[0], pos[1], INTERACTABLES)
        if tile != None:
            if "Can_Interact" in tile:
                if tile["Can_Interact"]:
                    if tile["type"] == "Red_lever":
                        tile["On"] = not tile["On"]
                        self.Change_tile_type_property("Red_door", "Open", tile["On"], STATIC_OBSTICLES)
                    elif tile["type"] == "Green_lever":
                        tile["On"] = not tile["On"]
                        self.Change_tile_type_property("Green_door", "Open", tile["On"], STATIC_OBSTICLES)
                    elif tile["type"] == "Blue_lever":
                        tile["On"] = not tile["On"]
                        self.Change_tile_type_property("Blue_door", "Open", tile["On"], STATIC_OBSTICLES)
    

    def conveyors(self,plr_pos, plr_rect):
        ##This function will check if the plr is standing on a conveyor and if so return the movemet direction
        ##Bottom Left
        BL = (int(plr_pos[0]/TILE_SIZE), int((plr_pos[1]+plr_rect[1]+2)/TILE_SIZE))## +2 is to chech tile plr is walking on
        ##Bottom Right
        BR = (int((plr_pos[0]+plr_rect[0])/TILE_SIZE), int((plr_pos[1]+plr_rect[1]+2)/TILE_SIZE))## +2 is to chech tile plr is walking on

        Check_tile = self.tmxdata.get_tile_properties(BL[0], BL[1], STATIC_OBSTICLES)
        if Check_tile != None:
            if "move_dir" in Check_tile:
                return Check_tile["move_dir"]
        
        Check_tile = self.tmxdata.get_tile_properties(BR[0], BR[1], STATIC_OBSTICLES)
        if Check_tile != None:
            if "move_dir" in Check_tile:
                return Check_tile["move_dir"]
        
        return 0 ##Plr is not standing on a conveyor


    def Change_tile_type_property(self, type :str, property :str, change_to :int, layer :int):
        ##This will search the intire map for tiles whit the same types on the given layer and
        ##chance the given property of those tiles to the given values
        for y in range(self.tmxdata.height):
            for x in range(self.tmxdata.width):
                tile = self.tmxdata.get_tile_properties(x, y, layer)
                if tile != None:
                    if "type" in tile:
                        if tile["type"] == type:
                            if property in tile:
                                tile[property] = change_to
    

    def Panning(self, axes:str, nom:int):

        # "l" = left
        # "r" = right
        # "t" = top
        # "b" = bottom
        amount = int(nom)
        if axes == "l" and amount < 0:
            self.offset_x += amount
            if self.offset_x < TILE_SIZE:
                self.offset_x -= amount
                return True
            
            elif self.offset_x > (self.tmxdata.width-31)*TILE_SIZE:
                self.offset_x -= amount
                return True
        elif axes == "r" and amount > 0:
            self.offset_x += amount
            if self.offset_x < TILE_SIZE:
                self.offset_x -= amount
            
            elif self.offset_x > (self.tmxdata.width-31)*TILE_SIZE:
                self.offset_x -= amount

        if axes == "t" and amount < 0:
            self.offset_y += amount
            if self.offset_y < TILE_SIZE:
                self.offset_y -= amount
            
            elif self.offset_y > (self.tmxdata.height-21)*16:
                self.offset_y -= amount

        elif axes == "b" and amount > 0:
            self.offset_y += amount
            if self.offset_y < TILE_SIZE:
                self.offset_y -= amount
            
            elif self.offset_y > (self.tmxdata.height-21)*16:
                self.offset_y -= amount


    def convert_map_to_list(self):
        ##This will convert each map layer into a list of all tile pos + gid
        for y in range (self.tmxdata.height):
            for x in range (self.tmxdata.width):
                ##Each list component is (x{without offset}, y{without offset}, tile_gid)
                tile_x = x
                tile_y = y


                
                # ##LEVERS
                # tile_proprerties = self.tmxdata.get_tile_properties(tile_x,
                #                                                     tile_y,
                #                                                     INTERACTABLES)
                # for l in self.lever_types:
                #     if tile_proprerties != None:
                #         if "type" in tile_proprerties:
                #             if tile_proprerties["type"] == l:
                #                 self.interact_list.append((x, y, self.tmxdata.get_tile_gid(tile_x, tile_y, INTERACTABLES)))
                
                ##DOORS
                tile_proprerties = self.tmxdata.get_tile_properties(tile_x,
                                                                    tile_y,
                                                                    FLOOR)
                for d in self.door_types:
                    if tile_proprerties != None:
                        if "type" in tile_proprerties:
                            if tile_proprerties["type"] == d:
                                self.active_tile_list.append((x, y, self.tmxdata.get_tile_gid(tile_x, tile_y, FLOOR)))
                
                # ##ANIMATIONS
                # tile_proprerties = self.tmxdata.get_tile_properties(tile_x,
                #                                                     tile_y,
                #                                                     ANIMATION_LAYER)
                # if tile_proprerties != None:
                #     self.animation_list.append((x, y, self.tmxdata.get_tile_gid(tile_x, tile_y, ANIMATION_LAYER)))
                
                # ##MIDGROUND
                # tile_image = self.tmxdata.get_tile_image(tile_x,
                #                                          tile_y,
                #                                          MIDGROUND)
                # if tile_image != None:
                #     self.mid_ground_list.append((x, y, self.tmxdata.get_tile_gid(tile_x, tile_y, MIDGROUND)))

                # ##DANGER TILES           
                # tile_image = self.tmxdata.get_tile_image(tile_x,
                #                                          tile_y,
                #                                          DANGER)
                # if tile_image != None:
                #     self.danger_list.append((x, y, self.tmxdata.get_tile_gid(tile_x, tile_y, DANGER)))

                ##PLATEFORMS            
                tile_image = self.tmxdata.get_tile_image(tile_x,
                                                         tile_y,
                                                         FLOOR)
                if tile_image != None:
                    self.platform_list.append((x, y, self.tmxdata.get_tile_gid(tile_x, tile_y, FLOOR)))
                if self.platform_list[0] == None:
                    self.platform_list.pop(0)


    def Exit_Check(self, plr_rect):
        ##plr_rect = ((map_x, map_y), (width, height))
        colliding = pygame.Rect.colliderect(plr_rect, self.exit_obj_rect)
        return colliding


if __name__ ==  "__main__":
    m = map(0,'')