from ursina import *
import numpy as np

class ShotGrid(Entity):
    def __init__(self,cli,**kwargs):
        Entity.__init__(self, position=(0,0,0), origin=(0,0,0),scale=(1,1),color=color.black50)
        self.grid = Entity(parent = self, scale=(10,10), model=Grid(10, 10),color=color.orange,position = (4.5,4.5))
        self.client = cli
        self.hit_cells = np.zeros(shape=(10,10),dtype=int)
        self.cells = \
        [
            [
                Entity(parent = self, model = "quad" , scale = (1,1),color=color.white33 ,collider="box")
                for x in range(10)
            ]
            for y in range(10)
        ]
        for x in range(10):
            for y in range(10):
                self.cells[x][y].position =(x , y)
        #print(self.cells)
        self.fixed = False
        self.shot_boutton = Button(text='Tirer', scale = (.1,.1), position = (-.5,0))
        self.shot_boutton.on_click = self.shot
        self.target = None
    
    def set_target_square(self,co):
        x,y = co
        cell = self.cells[x][y]
        if self.target != None:
            self.target.color = color.white33
        self.target = cell
        self.target_co = co
        self.target.color = color.white50
        
    def shot(self):
        self.client.shoot_at(self.target_co)
        self.hit_cells[self.target_co] = 1
        pass
    
    def shot_responce(self,hit):
        if hit:
            self.target.color = color.red
            Animation('assets/explosion.gif', loop=False,parent = self.target, z=-0.1)
        else:
            self.target.color = color.blue
            Animation('assets/eau.gif', loop=False,parent = self.target, z=-0.1)
        
        self.target = None

    def update(self):
        if self.target != None:
            self.shot_boutton.enabled = True
        else:
            self.shot_boutton.enabled = False


    def input(self,key):
        if key == 'left mouse down':
            if mouse.world_point is not None:
                pos = round(mouse.world_point)
                x,y = int(pos.x) , int(pos.y)
                #print(pos)
                if x in range(10) and y in range(10) and not self.hit_cells[x,y]:
                    self.set_target_square( (x,y) )
