from threading import Thread
import numpy as np
VECTOR = [np.array([1,0]),np.array([0,1])]
class Player:
    def __init__(self,ip,name="NoName"):
        self.name= name
        self.ip = ip
    def __repr__(self):
        return "%s : %s"% (self.name,self.ip)
class Ship:
    """Class to represent a ship"""
    def __init__(self, length) -> None:
        self.length = length
        self.hp = length
        self.position = None
        self.vec_id = 0
    def set(self,co,vec):
        pass
        
class Game(Thread):
    def __init__(self,player,x,y,serv):
        self.players = [player]
        self.serv =serv
        self.x_max = x
        self.y_max = y
        self.maps = np.zeros(shape = (2,x,y),dtype=bool)
        self.boats_set = set([Ship(i)for i in range(2,5)])
        self.stated = False
    def player_join(self,player):
        self.players.append(player)
        pass
    def place_boat(self,player,co,vec,lenght):
        player_id = self.players.index(player)
        for i in range(lenght):
            self.map[player_id, co[0] + i*vec[0],co[1] + i*vec[1]] = True
    def place_random_boat(self):
        pass
    def shoot(self,player,co):
        player_id = self.players.index(player)
        opp_id = (~player_id) +2
        
        if map[opp_id,co[0],co[1]]: # CIBLE TOUCHE
            self.serv.send(b"",self.players)
        else: # COULER
            self.serv.send(b"",self.players)
            pass
    def run():
        pass
