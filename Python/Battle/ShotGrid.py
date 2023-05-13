from ursina import *

class ShotGrid(Entity):
    def __init__(self,**kwargs):
        Entity.__init__(self, position=(0,0,0), origin=(0,0,0),scale=(1,1),color=color.black50)
        self.grid = Entity(parent = self, scale=(10,10), model=Grid(10, 10),color=color.orange,position = (4.5,4.5))
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
    
    def set_target_square(self,cell):
        if self.target != None:
            self.target.color = color.white33
        self.target = cell
        self.target.color = color.white50
        
    def shot(self):
        Animation('assets/explosion.gif', loop=False,parent = self.target)
        pass
    
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
                if x in range(10) and y in range(10):
                    self.set_target_square( self.cells[x][y] ) 
