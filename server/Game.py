from threading import Thread 
from Ship import Ship
import numpy as np
class Game(Thread):
    def __init__(self,player,x,y,serv):
        self.players = [player]
        self.serv =serv
        self.x_max = x
        self.y_max = y
        self.maps = np.zeros(shape = (2,x,y),dtype=int)
        self.boats_set = set([Ship(i)for i in range(2,7)])
        self.started = False
    def player_join(self,player):
        self.players.append(player)
        pass
    def place_boat(self,player,co,vec,lenght):
        player_id = self.players.index(player)
        for i in range(lenght):
            b = co[0] + i*vec[0],co[1] + i*vec[1]
            print("b = ",b)
            self.maps[player_id, b[0] , b[1]] = 1
    def place_random_boat(self,player_id):
        while len ( set.intersection( * [s.cells for s in self.boats_set] ) ) != 0:
            for s in self.boats_set:
                s.set_random()

        for s in self.boats_set:
            for cell in s.get_cells():
                self.maps[player_id, cell[0],cell[1]] = 1
    
    def shoot(self,player,co):
        player_id = self.players.index(player)
        opp_id = (~player_id) +2
        
        if self.maps[opp_id,co[0],co[1]]: # CIBLE TOUCHE
            self.serv.send(b"\x04\x01",self.players)
        else: # COULER
            self.serv.send(b"\x04\x00",self.players)
            pass
    def run():
        pass
    
    def __repr__(self):
        return str(self.maps)