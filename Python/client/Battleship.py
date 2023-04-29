import pygame as pg
import numpy as np
from threading import Thread
class BattleShip(Thread):
    def __init__(self,hauteur,longeur,name) -> None:
        Thread.__init__(self)
        self.screen = pg.display.set_mode(flags=pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.screen_size = self.screen.get_size()
        self.map_size = longeur,hauteur
        self.ratio_size = self.screen_size[0]/longeur,self.screen_size[1]/hauteur
        self.ratio = min(ratio_size)
        self.stop = False

    def run(self):
        while not self.stop:
            
            
            for event in pg.event.get():
                match event.type:
                    case pg.MOUSEBUTTONDOWN:
                        pass
                    case pg.MOUSEBUTTONUP:
                        pass
                    case pg.MOUSEMOTION:
                        pass
                    case pg.QUIT:
                        self.stop = True
            self.clock.tick(30) # 30 FPS
            pg.display.update()
