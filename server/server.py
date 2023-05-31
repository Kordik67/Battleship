import socket
import time
from threading import Thread
import numpy as np
from Player import *
from Ship import *
from Game import Game

class Server(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop = False
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.server.bind(("0.0.0.0", 4977))
        self.server.settimeout(2)
        self.players : dict[str, Player] = {}
        self.games_waiting : dict[str, Game] = {}
        self.games_runing : dict[str, Game] = {}
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
                            g = Game(player,10,10,self)
                            self.games_waiting[player.name] = g
                            new_game = b"\x00"
                            new_game += player.name.encode()
                            self.send_all(new_game)
                            player.game = g
                            pass
                        case 1: # JOIN GAME
                            name:bytes = message[1:]
                            if name in self.games_waiting:
                                self.games_waiting[name].player_join(player)

                                
                            pass
                        case 2: # SET PLAYER NAME
                            self.players[address[0]].name = message[1:].decode()
                            pass
                        case 3: # START GAME
                            start_game = b"\x01"

                            if message[1]: #PLAY VS AI
                                AI = Player(None,"AI")
                                g = self.games_waiting[player.name]
                                g.player_join(AI)
                                g.place_random_boat(1)
                            else: #PVP
                                pass
                            self.send(start_game,self.games_waiting[player.name].players)

                            self.games_runing[player.name] = self.games_waiting[player.name]
                            del self.games_waiting[player.name]

                        case 4: #PLACE BOAT
                            g = self.games_runing[player.name]
                            msg = message[1:]
                            for i in range(len(msg)//4):
                                x,y,dir_vec,lenght = msg[i*4 : i*4+4]
                                print(x,y,dir_vec,lenght)
                                g.place_boat(player, (x,y) ,VECTOR[dir_vec],lenght)
                        case 5: #REQUEST GAMES
                            pack = b"\x03"
                            pack += b"\x00".join([name.encode() for name in self.games_waiting.keys()])
                            pack += b"\x01"
                            pack += b"\x00".join([name.encode() for name in self.games_runing.keys()])
                            self.send(pack,[player])
                        case 6 : # SHOOT
                            x,y = message[1:3]
                            player.game.shoot(player,(x,y))
                            pass
            except socket.timeout:
                pass
            except socket.error as err:
                print("socket.errror",err)
    def send(self, o,players):
        for p in players:
            if p.name != "AI":
                self.server.sendto(o,p.ip)
    def send_all(self, o : bytes):
        for addr,player in self.players.items():
            if player.name != "AI":
                self.server.sendto(o,player.ip)


def main():
    serv = Server()
    serv.start()
    s = ""
    try:
        while s != "stop":
            s=input(":")
            print("player")
            print(serv.players)
            for k,v in serv.games_waiting.items():
                print(k,'\n', v)
            for k,v in serv.games_runing.items():
                print(k,'\n',v)
    except:
        pass
    serv.stop = True

if __name__ == '__main__':
    main()