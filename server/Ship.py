from random import randrange 


class Ship:
    """Class to represent a ship"""
    def __init__(self, length) -> None:
        self.length = length
        self.hp = length
        self.position = None
        self.set_random()
    def set_vec(self,id):
        self.vec_id = id
        self.vec = [0,0]
        self.vec[self.vec_id]+=1

    def set_random(self):
        self.set_vec(randrange(2))

        if self.vec_id:
            self.position =  (randrange(10),randrange(10-self.length))
        else:
            self.position =  (randrange(10-self.length),randrange(10))
        self.cells = set(self.get_cells())
        print("self.cells")
        print(self.cells)

    def get_cells(self):
        for i in range(self.length):
            yield (self.position[0] + self.vec[0]*i ,  self.position[1] + self.vec[1]*i)