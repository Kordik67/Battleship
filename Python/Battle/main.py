from ursina import *
from GameGrid import *
import numpy as np


app = Ursina()
window.borderless = False
camera.orthographic = True
camera.fov = 15
camera.position = (5, 5)
grille = GameGrid()



app.run()
