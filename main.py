
from genericpath import exists
from ursina import *
from controller import FirstPersonController
from manager import GameManager
import generator as gen

app = Ursina()


scene.fog_density = .05
scene.fog_color = color.white
#player = FirstPersonController(position=(0,0,0), origin_y=.5, gravity=0.5)
gm = GameManager()


app.run()

