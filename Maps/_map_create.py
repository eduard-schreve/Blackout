import shutil
import pathlib

BASEDIR = pathlib.Path(__file__).parent

template = pathlib.Path(BASEDIR.joinpath('Template.tmx'))
new_map = BASEDIR.joinpath(input('mapname => ')+'.tmx')
shutil.copy(template,new_map)
new_map.chmod(0o777)