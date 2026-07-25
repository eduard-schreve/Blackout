import pytmx
from globals import *
import pygame
import pathlib
import math

BASEDIR = pathlib.Path(__file__).parent

def Check_point_in_rect(point:Coord,rect:Rect) -> bool:
    TL = rect[0]
    BR = (rect[0][0]+rect[1][0],rect[0][1]+rect[1][1])
    if point[0] > TL[0] and point[0] < BR[0]:
        if point[1] > TL[1] and point[1] < BR[1]:
            return True
    return False


class MapNotLoadedError(Exception):
    """Error raised if the map operations are attempted before being loaded"""

class LevelControl():
    def __init__(self,map_pool:list[str],scn:pygame.surface.Surface):
        self.screen = scn
        self.map_pool = [str(BASEDIR.joinpath(p)) for p in map_pool]
        self.tmxdata = None
        self.offset_x = TILE_SIZE
        self.offset_y = TILE_SIZE


    def Load_map(self, m_index:int) -> None:
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
                if int(math.sqrt(m_y**2+m_x**2)+0.5) <= vision_dist:
                    tile_angle = math.degrees(math.atan2(m_y,m_x))+180

                    angle_min = angle-LIGHT_ANGLE if angle-LIGHT_ANGLE >= 0 else (360+angle-LIGHT_ANGLE)
                    angle_max = (angle+LIGHT_ANGLE)%360

                    flag_normal_boundries = tile_angle <= angle_max and tile_angle >= angle_min  ##Statement used in normal boundries where no wrapping around around 0-360 is required
                    flag_angle_min_wrap = angle_min > 360-(2*LIGHT_ANGLE) and tile_angle <= 360 and tile_angle >= angle_min  ##Statement used if angle_min wraps around 0-360 to the 360 side
                    flag_angle_max_wrap = angle_max < 2*LIGHT_ANGLE and tile_angle <= angle_max and tile_angle >= 0  ##Statementused if angle_max wraps around 0-360 to the 0 side
                    if flag_normal_boundries or flag_angle_min_wrap or flag_angle_max_wrap:  #The statement from hell allowing the spinny light to fully wrap arround the 0-360 point correctly
                        vis_tiles.add((m_x+plr_tile[0],m_y+plr_tile[1]))
        return vis_tiles

    def Get_obj(self,name:str):
        if self.tmxdata == None:
            MapNotLoadedError('Map has not been loaded')
            return
        return self.tmxdata.get_object_by_name(name)


    def Collisions(self,obj:Rect) -> list[Rect]:
        colliders = []
        if self.tmxdata == None:
            MapNotLoadedError('Map has not been loaded')
            return False
        obj_tile_pos = (obj[0]//TILE_SIZE,obj[1]//TILE_SIZE)
        self.tmxdata.tilesets
        for layer_index in range(len(self.tmxdata.layernames)):
            if getattr(self.tmxdata.layers[layer_index], 'class') == 'obj':
                continue
            for y in range(-1,2):
                for x in range(-1,2):
                    if x==y==0:
                        continue
                    map_x = obj_tile_pos[0]+x
                    map_y = obj_tile_pos[1]+y
                    properties = self.tmxdata.get_tile_properties(map_x,map_y,layer_index)
                    if properties != None:
                        rect = (map_x*TILE_SIZE+properties['colliders'][0].x,
                                map_y*TILE_SIZE+properties['colliders'][0].y,
                                properties['colliders'][0].width,
                                properties['colliders'][0].height)
                        colliders.append(rect)
        return colliders
                    