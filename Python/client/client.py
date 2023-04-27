from pygame import *
from tkinter import ttk
from tkinter import *
import sys
import socket
from Ship import Ship
from App import App

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '82.64.91.183'#'network.freeboxos.fr'
port = 4777
print(server.sendto(b"Yoo", (host, port)))

def main() -> int:
    #App(Tk(), server)
    return 0


if __name__ == '__main__':
    sys.exit(main())
