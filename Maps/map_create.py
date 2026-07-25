import pathlib
BASEDIR = pathlib.Path(__file__).parent
with open(BASEDIR.joinpath(input('File Name: ')+'.tmx'),'w') as file:
    file.writelines(['<?xml version="1.0" encoding="UTF-8"?>',
     '<map version="1.10" tiledversion="1.11.0"',
     'orientation="orthogonal"',
     'width="40"',
     'height="40"',
     'tilewidth="32"',
     'tileheight="32">',
     '<tileset firstgid="1" source="TileMaps/Basic_Tiles.tsx"/>',
     '<layer name="Decor" class="decor"/>',
     '<layer name="Static_Obstacles" class="collision"/>',
     '<layer name="Floor" class="ground"/>',
     '<objectgroup name="Lvl_Data" class="obj"/>',
     '<objectgroup name="Wires" class="obj"/>',
     '</map>'])