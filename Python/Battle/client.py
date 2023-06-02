import socket
from ursina import *
from threading import Thread
from GameGrid import GameGrid

class Client(Thread):
    def __init__(self, main_menu=None, game_grid=None, shoot_grid=None):
        Thread.__init__(self)
        self.main_menu = main_menu
        self.game_grid = game_grid
        self.shoot_grid = shoot_grid

        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.settimeout(2)
        self.host = "network.freeboxos.fr"
        #self.host = "localhost"
        self.port = 4977
        self.send(b'Connected')
        msg, addr = self.server.recvfrom(1024)
        if msg[0] == 0:  # PAS DE PSEUDO ENREGISTERER
            self.named = False
        else:
            self.named = True
            self.name = msg.decode()
        self.stop = False

    def send(self, o: bytes):
        self.server.sendto(o, (self.host, self.port))

    def setName(self, name: str):
        self.name = name
        self.send(b"\x02"+name.encode())

    def createGame(self):
        self.send(b"\x00")

    def joinGame(self, name: str):
        self.send(b"\x01"+name.encode())

    def startGame(self, ai: bool):
        self.send(b"\x03" + b"\x01" if ai else b"\x00")

    def placeBoat(self, x: int, y: int, dir_vec: int, lenght: int):
        self.send(bytes([x, y, dir_vec, lenght]))

    def requestGames(self):
        self.send(b"\x05")

    def shoot_at(self, co):
        self.send(b"\x06%c%c" % co)

    def delete_game(self):
        self.send(b"\x07")

    def run(self) -> None:
        while not self.stop:
            try:
                msg, addr = self.server.recvfrom(1024)
                print("recv msg from server", addr, "|", msg)

                match msg[0]:
                    case 0:  # NEW GAME CREATED
                        # name = msg[1:]
                        # self.app.new_game(name)
                        pass
                    case 1:  # GAME STARTED
                        # x = msg[1]
                        # y = msg[2]
                        # self.battle = BattleShip(x,y)
                        # self.battle.start()
                        self.game_grid = GameGrid(self)
                    case 2:  # GAME ENDED
                        # name = msg[1:]
                        pass
                    case 3:  # GAME ROOM UPDATE
                        # Format : "\x03nom1\x00nom2\x00nom3\x01nom1\x00"
                        waiting, playing = msg[1:].split(b'\x01')
                        waiting_rooms = [s.decode() for s in waiting.split(b'\x00')]
                        playing_rooms = [s.decode() for s in playing.split(b'\x00')]

                        print("waiting :", waiting_rooms)
                        print("Playing :", playing_rooms)

                        self.main_menu.create_rooms_list(
                            waiting_rooms, playing_rooms)
                    case 4:  # SHOOT RESPONCE
                        hited, x, y = msg[1:]
                        print("HITED (%d,%d)" % (x, y), hited)
                        if self.shoot_grid.client_turn:
                            self.shoot_grid.shot_responce(hited)
                        else:
                            self.game_grid.fired(hited, (x, y))
                            self.shoot_grid.client_turn = not hited
            except socket.timeout:
                pass
