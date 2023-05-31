from threading import Thread
import numpy as np
VECTOR = [np.array([1,0]),np.array([0,1])]
class Player:
    def __init__(self,ip,name="NoName",game=None):
        self.name= name
        self.ip = ip
        self.game = game
    def __repr__(self):
        return "%s : %s"% (self.name,self.ip)
