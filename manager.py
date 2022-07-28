from ursina import *
import generator as gen
import time
from controller import FirstPersonController

class Cube(Entity):
    def __init__(self, parent, position=(0,0,0), color=color.color(0, 0, random.uniform(.9, 1.0))):
        super().__init__(
            parent = parent,
            position = (2*position[0],2*position[1], 2*position[2]),
            model = 'cube',
            origin_y = .5,
            texture = 'white_cube',
            color = color,
            scale = (2,2,2)
        )

class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.level_parent = Entity(model=None)
        self.level_parent.name = 'level_geom'
        self.items = Entity(model=None)
        self.items_hash = {}
        self.mp = gen.gen_map(40, 40, 10, 10, 5)
        self.player = FirstPersonController(parent=self.level_parent, position=(0,0,0), origin_y=.5)
        self.player.position = self.render_map()

    def change_level(self):
        destroy(self.level_parent)
        destroy(self.items)
        destroy(self.player)
        self.player = FirstPersonController(parent=self.level_parent, position=(0,0,0), origin_y=.5)
        self.level_parent = Entity(model=None)
        self.level_parent.name = 'level_geom'
        self.level_parent.model = None
        self.items = Entity(model=None)
        self.items_hash = {}
        self.mp = gen.gen_map(20, 20, 10, 10, 2)

        self.render_map()

    
    def render_map(self):
        for i, row in enumerate(self.mp):
            for j, block in enumerate(row):
                if block == '.':
                    Cube(parent = self.level_parent, position = (i,0,j))
                    Cube(parent = self.level_parent, position = (i,3,j))
                elif block == 'w':
                    Cube(parent = self.level_parent, position = (i,1,j))
                    Cube(parent = self.level_parent, position = (i,2,j))
                    Cube(parent = self.level_parent, position = (i,3,j))
                elif block == 'p':
                    Cube(parent = self.level_parent, position = (i,0,j))
                    self.player.position = Vec3(2*i,0,2*j)
                    print('DONE')
                elif block == 'e':
                    exit_marker = Cube(parent=self.items, position=(i,1,j), color=color.red)
                    exit_marker.collider = 'box'
                    exit_marker.name = 'exit'
                    self.items_hash[exit_marker.name] = Vec3(2*i,0,2*j)

        self.level_parent.combine()
        self.level_parent.collider = 'mesh'
        self.level_parent.texture = 'white_cube'
    
    def input(self, key):
        if key == 'o':
            exit()

    def update(self):
        if 'exit' in self.items_hash.keys():
            if self.player.position == self.items_hash['exit']:
                self.change_level()
    
