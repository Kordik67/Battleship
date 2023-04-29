import socket
import time
from threading import Thread
import numpy as np
from BattleShipCore import *

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
                            g = Game(player,message[1],message[2],self)
                            self.games[player.name] = g
                            new_game = b"\x00"
                            new_game += player.name.encode()
                            self.send_all(new_game)
                            pass
                        case 1: # JOIN GAME
                            name:bytes = message[1:]
                            if name in self.games:
                                self.games[name].player_join(player)

                                
                            pass
                        case 2: # SET PLAYER NAME
                            self.players[address[0]].name = message[1:].decode()
                            pass
                        case 3: # START GAME
                            game_start = b"\x01"
                            game_start += player.name.encode()

                            if message[1]: #PLAY VS AI
                                AI = Player(None,"AI")
                                self.games[player.name].player_join(AI)
                            else: #PVP

                            pass
                        case 4 #PLACE BOAT
                            pass
            except socket.timeout:
                pass
    def send(self, o,players):
        for p in players:
            if p.name != "AI":
                self.server.send(o,p.id)
    def send_all(self, o : bytes):
        for addr,player in self.players.items():
            if p.name != "AI":
                self.server.sendto(o,player.ip)


def main():
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

if __name__ == '__main__':
    main()