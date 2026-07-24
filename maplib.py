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
        # delta_mouse_pos = (plr_pos[0]-point_pos[0],plr_pos[1]-point_pos[1])
        point_angle = math.degrees(math.atan2(delta_mouse_pos[1],delta_mouse_pos[0]))+180
        print(point_angle)
        vis_mask = self._generate_visible_mask(point_angle,5,plr_tile_pos)

        for layer in self.tmxdata.layers:
            if getattr(layer,"class") == "obj":
                continue
            else:
                tiles = layer.tiles()
                for x,y,img in tiles:
                    if (x,y) in vis_mask:
                        self.screen.blit(img,(x*TILE_SIZE,y*TILE_SIZE))
                
             

    def _generate_visible_mask(self,angle:float,vision_dist:int,plr_tile:Coord) -> set[Coord]:
        vis_tiles = set()
        vis_tiles.add(plr_tile)
        for y in range(vision_dist*2+1):
            for x in range(vision_dist*2+1):
                m_y = y - vision_dist
                m_x = x -vision_dist
                if math.sqrt(m_y**2+m_x**2) <= vision_dist:
                    tile_angle = math.degrees(math.atan2(m_y,m_x))+180

                    angle_min = angle-LIGHT_ANGLE if angle-LIGHT_ANGLE >= 0 else (360+angle-LIGHT_ANGLE)
                    angle_max = (angle+LIGHT_ANGLE)%360

                    flag_normal_boundries = tile_angle <= angle_max and tile_angle >= angle_min  ##Statement used in normal boundries where no wrapping around around 0-360 is required
                    flag_angle_min_wrap = angle_min > 360-(2*LIGHT_ANGLE) and tile_angle <= 360 and tile_angle >= angle_min  ##Statement used if angle_min wraps around 0-360 to the 360 side
                    flag_angle_max_wrap = angle_max < 2*LIGHT_ANGLE and tile_angle <= angle_max and tile_angle >= 0  ##Statementused if angle_max wraps around 0-360 to the 0 side
                    if flag_normal_boundries or flag_angle_min_wrap or flag_angle_max_wrap:  #The statement from hell allowing the spinny light to fully wrap arround the 0-360 point correctly
                        vis_tiles.add((m_x+plr_tile[0],m_y+plr_tile[1]))
        return vis_tiles

    def get_obj(self,name:str):
        if self.tmxdata == None:
            MapNotLoadedError('Map has not been loaded')
            return
        return self.tmxdata.get_object_by_name(name)
