import socket
import time
from threading import Thread
import numpy as np

class Player:
    def __init__(self,ip):
        self.name= "NoName"
        self.ip = ip
        
class Game:
    def __init__(self,player,x,y):
        self.players = [player]
        self.x_max = x
        self.y_max = y
        self.maps = np.zeros(shape = (2,x,y),dtype=bool)
    def player_join(self,player):
        self.players.append(player)
        pass
    def place_boat(self,player,co,vec,lenght):
        player_id = self.players.index(player)
        for i in range(lenght):
            self.map[player_id, co[0] + i*vec[0],co[1] + i*vec[1]] = True
    def shoot(self,player,co):
        global serv
        player_id = self.players.index(player)
        opp_id = (~player_id) +2
        
        if map[opp_id,co[0],co[1]]: # CIBLE TOUCHE
            serv.send(b"",self.players)
        else: # COULER
            serv.send(b"",self.players)
            pass

class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind(("0.0.0.0", 4977))
        self.server.settimeout(2)
        self.players : dict[str, Player] = {}
        self.games : dict[str, Game] = {}
    def run(self):
        while not self.stop:
            try:
                message , address = self.server.recvfrom(4096)
                print("address",address)
                print("message",message)
                if message == b'Connected':
                    if address[0] not in self.players:
                        self.server.sendto(bytes(1), address)
                        self.players[address[0]] = Player(address)

                    else:
                        p = self.players[address[0]]
                        self.server.sendto(p.name.encode(), address)

                else:
                    player = self.players[address[0]]
                    match message[0]:
                        case 0: # CREATE GAME
                            g = Game(player,message[1],message[2])
                            self.games[player.name] = g
                            new_game = b"\x00"
                            new_game += player.name.encode()
                            self.send_all(new_game)
                            pass
                        case 1: # JOIN GAME
                            name:bytes = message[1:]
                            if name in self.games:
                                self.games[name].player_join(player)
                                game_start = b"\x01"
                                game_start += name.encode()

                                
                            pass
                        case 2: # SET PLAYER NAME
                            self.players[address[0]].name = message[1:].decode()
                            pass
                        case 0: # CREATE GAME
                            pass
            except socket.timeout:
                pass
    def send(self, o,players):
        for p in players:
            self.server.send(o,p.id)
    def send_all(self, o : bytes):
        for addr,player in self.players.items():
            self.server.sendto(o,player.ip)

serv = Server()

def main():
    global serv
    serv.start()
    s = ""
    try:
        while s != "stop":
            s=input(":")
            print(serv.players)
    except:
        pass
    serv.stop = True

if __name__ == '__main__':
    main()