from tkinter import Tk
import sys
import socket
from Ship import Ship
from App import App

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = 'network.freeboxos.fr'
port = 4977
  

def main() -> int:
    app = App(server, host, port)
    app.start()
    input()

    app.serv.stop = True
    return 0


if __name__ == '__main__':
    sys.exit(main())
