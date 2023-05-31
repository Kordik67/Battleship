from ursina import *
from GameGrid import *
from Menu.MainMenu import MainMenu
from client import Client

def starter(cli):
    window.borderless = False
    camera.orthographic = True
    camera.fov = 15
    camera.position = (5, 5)
    grille_jeu = GameGrid(cli)
    cli.game_grid = grille_jeu
    #grid = Entity(scale=(10,10), model=Grid(10, 10),color=color.orange,position = (4.5,4.5))


if __name__ == "__main__":
    app = Ursina()
    cli = Client()
    main_menu = MainMenu(start_callback=starter,client=cli)
    cli.main_menu = main_menu
    cli.start()
    app.run()