
from ursina import *
from controller import FirstPersonController
import generator as gen

app = Ursina()

level_parent = Entity(model=None)


class Cube(Entity):
    def __init__(self, parent=level_parent, position=(0,0,0)):
        super().__init__(
            parent = parent,
            position = (2*position[0],2*position[1], 2*position[2]),
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color.color(0, 0, random.uniform(.9, 1.0)),
            scale = (2,2,2)
        )

def render_map(mp, parent):
    player_loc = (0,0,0)
    for i, row in enumerate(mp):
        for j, block in enumerate(row):
            if block == '.':
                Cube(position=(i,0,j))
                Cube(position=(i,3,j))
            if block == 'w':
                Cube(position=(i,1,j))
                Cube(position=(i,2,j))
                Cube(position=(i,3,j))
            if block == 'p':
                Cube(position=(i,0,j))
                player_loc = (2*i,0,2*j)
               
    parent.combine()
    parent.collider = 'mesh'
    parent.texture = 'white_cube'

    return player_loc

mp = gen.gen_map(40,40, 10, 10, 5)
player_loc = render_map(mp, level_parent)

def input(key):
    if key == 'o':
        exit()

#EditorCamera()
scene.fog_density = .05
scene.fog_color = color.white
player = FirstPersonController(position=player_loc, origin_y=.5, gravity=0.5)

app.run()

