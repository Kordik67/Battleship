import socket
from ursina import *
from GameGrid import *

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "network.freeboxos.fr"
port = 4977

def main():
    window.borderless = False
    camera.orthographic = True
    camera.fov = 15
    camera.position = (5,5)
    grid = GameGrid()

if __name__ == "__main__":
    app = Ursina()
    main()
    app.run()