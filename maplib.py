import pytmx
from globals import *
import pygame
import pathlib
import math

BASEDIR = pathlib.Path(__file__).parent

class MapNotLoadedError(Exception):
    """Error raised if the map operations are attempted before being loaded"""

class LevelControl():
    def __init__(self,map_pool:list[str],scn:pygame.surface.Surface):
        self.screen = scn
        self.map_pool = [str(BASEDIR.joinpath(p)) for p in map_pool]
        self.tmxdata = None
        self.offset_x = TILE_SIZE
        self.offset_y = TILE_SIZE


    def load_map(self, m_index:int) -> None:
        self.tmxdata = pytmx.load_pygame(self.map_pool[m_index])

    def Render_map(self, plr_pos:Coord, point_pos:Coord) -> None:
        if self.tmxdata == None:
            if self.tmxdata == None:
                        MapNotLoadedError('Map has not been loaded')
                        return
        plr_tile_pos = (plr_pos[0]//TILE_SIZE,plr_pos[1]//TILE_SIZE)
        delta_mouse_pos = (point_pos[0]-plr_pos[0],point_pos[1]-plr_pos[1])
        delta_mouse_pos = (plr_pos[0]-point_pos[0],plr_pos[1]-point_pos[1])
        point_angle = math.degrees(math.atan2(delta_mouse_pos[0],delta_mouse_pos[1]))
        print(f"Point: {point_angle}")
        vis_mask = self._generate_visible_mask(point_angle,5,plr_tile_pos)
        print(len(vis_mask))

        for layer in self.tmxdata.layers:
            if getattr(layer,"class") == "obj":
                continue
            else:
                tiles = layer.tiles()
                for x,y,img in tiles:
                    if (x,y) in vis_mask:
                        self.screen.blit(img,(x*TILE_SIZE,y*TILE_SIZE))
                
             

    def _generate_visible_mask(self,angle:float,vision_dist:int,plr_tile:Coord) -> list[Coord]:
        vis_tiles = []
        for y in range(vision_dist*2+1):
            for x in range(vision_dist*2+1):
                y = y - vision_dist//2
                x = x -vision_dist//2
                tile_angle = math.degrees(math.atan2(y,x))
                if tile_angle <= angle+LIGHT_ANGLE and tile_angle >= angle-LIGHT_ANGLE:
                    vis_tiles.append((x+plr_tile[0],y+plr_tile[1]))
        return vis_tiles

    def get_obj(self,name:str):
        if self.tmxdata == None:
            MapNotLoadedError('Map has not been loaded')
            return
        return self.tmxdata.get_object_by_name(name)
