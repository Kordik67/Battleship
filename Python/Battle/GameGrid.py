from ursina import *
import numpy as np
from Ships.ships import *
from ShotGrid import *
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
        self.fixed = False
        self.ready_boutton = Button(text='Pret', scale = (.1,.1), position = (-.5,0))
        self.ready_boutton.on_click = self.ready

        self.ships =[
            Ship("Carrier", 5,parent = self),
            Ship("Battleship", 4,parent = self),
            Ship("Cruiser", 3,parent = self),
            Ship("Submarine", 2,parent = self),
            Ship("Destroyer", 1,parent = self)
        ]
        
    def ready(self):
        self.ready_boutton.enabled = False
        for s in self.ships:
            s.fixed = True
        self.fixed = True
        #self.position = (12,7.5)
        #self.scale = (.5,.5)
        #self.animate("position", (12,7.5),duration=3)
        self.animate("scale", (.5,.5),duration=2)
        #self.animate_scale((.5,.5),duration=3,delay=3)
        self.animate_position((12,7.5),duration=2,delay=0)
        ShotGrid()        
        pass

    def update(self):

        if not self.fixed:
            if all([ship.is_valid_placement() for ship in self.ships]):
                self.ready_boutton.enabled = True
            else:
                self.ready_boutton.enabled = False
