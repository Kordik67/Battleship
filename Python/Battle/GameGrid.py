from ursina import *
import numpy as np
from ships import *
class GameGrid(Entity):
    def __init__(self,**kwargs):
        Entity.__init__(self, position=(0,0,0), origin=(0,0,0),scale=(1,1),color=color.black50)
        self.grid = Entity(parent = self, scale=(10,10), model=Grid(10, 10),color=color.orange,position = (4.5,4.5))
        self.cells = \
        [
            [
                Entity(parent = self, model = "quad" , scale = (1,1),color=color.azure ,collider="box")
                for x in range(10)
            ]
            for y in range(10)
        ]
        for x in range(10):
            for y in range(10):
                self.cells[x][y].position =(x , y)
        #print(self.cells)

        self.ships =[
            Ship("Carrier", 5,parent = self),
            Ship("Battleship", 4,parent = self),
            Ship("Cruiser", 3,parent = self),
            Ship("Submarine", 2,parent = self),
            Ship("Destroyer", 1,parent = self)
        ]
        