import pytmx
from globals import *
import pygame
import pathlib
import math

BASEDIR = pathlib.Path(__file__).parent

<<<<<<< HEAD
=======
def Sort_by_id(layer):
    return layer.id


>>>>>>> 8b709ff (Allowed Interation with objects on the Interact maplayer)
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
<<<<<<< HEAD
        delta_mouse_pos = (plr_pos[0]-point_pos[0],plr_pos[1]-point_pos[1])
        point_angle = math.degrees(math.atan2(delta_mouse_pos[0],delta_mouse_pos[1]))
        print(f"Point: {point_angle}")
        vis_mask = self._generate_visible_mask(point_angle,5,plr_tile_pos)
        print(len(vis_mask))

        for layer in self.tmxdata.layers:
=======
        # delta_mouse_pos = (plr_pos[0]-point_pos[0],plr_pos[1]-point_pos[1])
        point_angle = math.degrees(math.atan2(delta_mouse_pos[1],delta_mouse_pos[0]))+180
        vis_mask = self._generate_visible_mask(point_angle,vis_dist,plr_tile_pos)
        # print(self.tmxdata.layers)
        sorted_layers = sorted(self.tmxdata.layers,key=Sort_by_id)
        for layer in sorted_layers:
>>>>>>> 8b709ff (Allowed Interation with objects on the Interact maplayer)
            if getattr(layer,"class") == "obj":
                if layer.name == 'Wires':
                    wire_lines ={}
                    for node in layer:
                        if not node.name in wire_lines:
                            wire_lines[node.name] = []
                        wire_lines[node.name].append((node.x,node.y))
                    for key in wire_lines.keys():
                        pygame.draw.lines(self.screen,(255,0,0),False,wire_lines[key])
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
<<<<<<< HEAD
=======


    def Exec_func_str(self,func_str:str) -> bool:
        if self.tmxdata == None:
                    MapNotLoadedError('Map has not been loaded')
                    return False
        parced = func_str.split(' ')
        if parced[0] == "setb": #Set Boolean Value
            obj = self.tmxdata.get_object_by_id(int(parced[1]))
            if parced[3] == "True":
                obj.properties[parced[2]] = True
            else:
                obj.properties[parced[2]] = False
        return True


    def Interact(self,plr:Rect):
        plr_rect = pygame.rect.Rect(plr)
        if self.tmxdata == None:
            MapNotLoadedError('Map has not been loaded')
            return
        for layer in self.tmxdata.layers:
            layer_prop = layer.properties
            if 'interact' in layer_prop and layer_prop['interact']:
                for obj in layer:
                    obj_prop = obj.properties
                    obj_rect = (obj.x,obj.y,obj.width,obj.height)
                    if plr_rect.colliderect(obj_rect) and 'function' in obj_prop:
                        print('Pressed')
                        self.Exec_func_str(obj_prop['function'])


    def Collisions(self,obj:Rect) -> list[Rect]:
        colliders = []
        if self.tmxdata == None:
            MapNotLoadedError('Map has not been loaded')
            return []
        obj_tile_pos = (obj[0]//TILE_SIZE,obj[1]//TILE_SIZE)
        self.tmxdata.tilesets
        for layer_index in range(len(self.tmxdata.layernames)):
            if getattr(self.tmxdata.layers[layer_index], 'class') == 'obj':
                for collider_obj in self.tmxdata.layers[layer_index]:
                    if "collide" in collider_obj.properties and collider_obj.properties["collide"] == True:
                        rect = (collider_obj.x,
                                collider_obj.y,
                                collider_obj.width,
                                collider_obj.height)
                        colliders.append(rect)
            else:
                for y in range(-1,2):
                    for x in range(-1,2):
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
                    
>>>>>>> 8b709ff (Allowed Interation with objects on the Interact maplayer)
