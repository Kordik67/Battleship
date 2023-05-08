from ursina import *
from MyDrag import MyDraggable

class Ship(MyDraggable):
    def __init__(self,name,lenght,**kwargs):
        super().__init__(color=(0,0,0),collider="box",**kwargs)
        self.paire = lenght % 2 == 0
        self.direction = random.randrange(2)
        if self.direction == 0:
            self.scale = (lenght,1)
        else:
            self.scale = (1,lenght)
        
        self.lenght = lenght
        self.update_boarder()
        self.name = name
        
        self.position = (random.randint(self.min_x, self.max_x),random.randint(self.min_y, self.max_y),-.1)
        
        self.snap_to_grid()
        
        self.set_cell_set()
        

        for c in self.cells:
            print(c)
            self.parent.cells[int(c.x)][int(c.y)].color = color.blue

    def update_boarder(self):
        self.min_x = self.scale[0]//2 + ( -1 if self.paire and self.direction == 0 else 0 )
        self.min_y = self.scale[1]//2 + ( -1 if self.paire and self.direction == 1 else 0 ) 
        self.max_x = 9 - self.scale[0]//2 + 0.0
        self.max_y = 9 - self.scale[1]//2 + 0.0
        print(self.min_x,self.min_y,self.max_x,self.max_y, "|",self.lenght)
    def snap_to_grid(self):
        if self.lenght&1: # si la taille est impaire
            self.position = int(self.position[0]), int(self.position[1]) , -.1
        else:
            if self.scale[0] > self.scale[1]: # SENS HORIZONTALE
                self.position = int(self.position[0]) + .5, int(self.position[1]) , -.1
            else: # SENS VERTICALE
                self.position = int(self.position[0]) , int(self.position[1]) + .5 , -.1

    def pos_on(self):
        pos = Vec2( int(self.x) , int(self.y) )
        dir = Vec2(0,0)
        dir[self.direction] +=1
        yield pos
        if self.paire:
            for i in range( (self.lenght//2) -1 ):
                yield pos + ((i+1)*dir)
                yield pos + ((-i-1)*dir) 
            yield pos + ((self.lenght//2)*dir)

        else:
            for i in range(self.lenght//2):
                yield pos + ((i+1)*dir)
                yield pos + ((-i-1)*dir) 

    def set_cell_set(self):
        self.cells = set(self.pos_on())

    def drag(self):
        print("DRAG",mouse.position)
        self.parent.dragged_ship = self
        pass
    def drop(self,**kwargs):
        print("DROP",mouse.position)
        self.parent.dragged_ship = None
        #self.position = self.org_pos
        #print(type(mouse.hovered_entity))
        #self.snap_to_grid()
        pass
    def input(self, key):
        #print(self.name,key)
        super().input(key)
        if self.dragging and key == 'right mouse down':
            print("Rotate")
            sc = self.scale
            self.scale = sc[1],sc[0]
            self.direction = int(not self.direction)
            self.update_boarder()

            #self.rotation_y += 90
    def update(self):
        super().update()
        if self.dragging:
            self.snap_to_grid()
            #print("pos %.2f %.2f %.2f"%(self.x,self.y,self.z))
            #print(set(self.pos_on()))
