from ursina import *
from GameGrid import *



def start():
    window.borderless = False
    camera.orthographic = True
    camera.fov = 15
    camera.position = (5, 5)
    grille = GameGrid()
    #grid = Entity(scale=(10,10), model=Grid(10, 10),color=color.orange,position = (4.5,4.5))


if __name__ == "__main__":
    app = Ursina()
    start()
    app.run()