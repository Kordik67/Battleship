from ursina import *

class Ship(Draggable):
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
        
        self.position = (random.randint(self.min_x, int(self.max_x)),random.randint(self.min_y, int(self.max_y)),-.1)
        
        self.snap_to_grid()
        
        self.set_cell_set()
        
        self.tooltip = Tooltip(self.name)

        self.fixed = False


    def update_boarder(self):
        self.min_x = self.scale[0]//2 + ( -1 if self.paire and self.direction == 0 else 0 )
        self.min_y = self.scale[1]//2 + ( -1 if self.paire and self.direction == 1 else 0 ) 
        self.max_x = 9 - self.scale[0]//2 + 0.5
        self.max_y = 9 - self.scale[1]//2 + 0.5
        print(self.min_x,self.min_y,self.max_x,self.max_y, "|",self.lenght)
    def snap_to_grid(self):
        if self.paire:
            if self.scale[0] > self.scale[1]: # SENS HORIZONTALE
                self.position = int(self.position[0]) + .5, int(self.position[1]) , -.1
            else: # SENS VERTICALE
                self.position = int(self.position[0]) , int(self.position[1]) + .5 , -.1
        else:
            self.position = int(self.position[0]), int(self.position[1]) , -.1

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
        self.cells : set  = set(self.pos_on())

    def drag(self):
        self.parent.dragged_ship = self
        pass
    def drop(self,**kwargs):
        self.parent.dragged_ship = None
        #self.position = self.org_pos
        #print(type(mouse.hovered_entity))
        self.snap_to_grid()
        pass
    def input(self, key):
        #print(self.name,key)
        if self.fixed:
            return
        super().input(key)
        if self.dragging and key == 'right mouse down':
            print("Rotate")
            sc = self.scale
            self.scale = sc[1],sc[0]
            self.direction = int(not self.direction)
            self.update_boarder()

            #self.rotation_y += 90
    def update(self):
        if self.fixed:
            return
        super().update()
        if self.dragging:
            self.snap_to_grid()
            self.set_cell_set()
            #print("pos %.2f %.2f %.2f"%(self.x,self.y,self.z))
            #print(self.cells)


        if self.is_valid_placement():
            self.color = color.black50
        else:
            self.color = Color(1,0,0,.5) # RED
    def is_valid_placement(self):
        for s in self.parent.ships:
            if s is not self:
                if len( s.cells.intersection(self.cells) ) != 0:
                    return False
        return True