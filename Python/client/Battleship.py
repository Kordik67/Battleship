import pygame as pg
import numpy as np
from threading import Thread
class BattleShip:
    def __init__(self,longeur,hauteur) -> None:
        self.screen = pg.display.set_mode(flags=pg.FULLSCREEN)
        self.clock = pg.time.Clock()
        self.screen_size = np.array(self.screen.get_size())
        self.map_size = np.array([longeur,hauteur])
        self.ratio_size = self.screen_size/self.map_size
        self.ratio = min(self.ratio_size)
        self.map_size_px = self.map_size * self.ratio

        self.stop = False
        self.i = 0
        Thread.__init__(self)
    def run(self):
        while not self.stop:
            self.screen.fill((250,250,250))

            for x in range(self.map_size[0]):
                for y in range(self.map_size[1]):
                    pg.draw.rect(self.screen, (0,0,0),
                    ( self.i + (self.screen_size[0] - self.map_size_px[0])/2 + x * self.ratio  , (self.screen_size[1] - self.map_size_px[1])/2 + y * self.ratio
                    , self.ratio,self.ratio),width=2)
            
            for event in pg.event.get():
                print(event)
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
            self.i+=1

if __name__ == "__main__":
    pg.init()
    BattleShip(10, 10).start()
    #pg.mainloop()
    input("FINFINFINFINFINFINFINFINFINFINFINFINFINFINFIN")
    pg.quit()