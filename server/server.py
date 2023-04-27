import socket
import time
from threading import Thread
class Player:
    def __init__(self,name,ip):
        self.name= name
        self.ip = ip
class Game:
    def __init__(self,player,x,y):
        self.player = player
        self.x = x
        self.y = y
    def player_join(self,player):
        pass

class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind(("0.0.0.0", 4977))
        self.server.settimeout(2)
        self.players = {}

    def run(self):
        while not self.stop:
            try:
                message , address = self.server.recvfrom(4096)
                print("address",address)
                print("message",message)
                if address not in self.players:
                    self.players[address] = Player(message.decode(), address)
                else:
                    player = self.players[address]
                    match message[0]:
                        case 0: # CREATE GAME
                            g = Game(player,message[1],message[2])
                            pass
                        case 1: # JOIN GAME
                            pass
                        case 2:
                            pass

            except socket.timeout:
                pass

serv = Server()
serv.start()
s = ""
try:
    while s != "stop":
        s=input(":")
        print(serv.players)
except:
    pass
serv.stop = True
