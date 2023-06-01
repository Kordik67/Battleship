from threading import Thread

import numpy as np

from Ship import Ship
from Player import Player


class Game(Thread):
    def __init__(self, player, x, y, serv):
        self.players = [player]
        self.serv = serv
        self.x_max = x
        self.y_max = y
        self.maps = np.zeros(shape=(2, x, y), dtype=int)
        self.boats_list = [Ship(i)for i in range(2, 7)]
        self.boats_set = set(self.boats_list)
        self.started = False
        self.current_player_id = 0

    def player_join(self, player):
        if isinstance(player, Player):
            self.players.append(player)
        else:
            self.ai = player

    def place_boat(self, player, co, vec, lenght):
        player_id = self.players.index(player)
        for i in range(lenght):
            b = co[0] + i*vec[0], co[1] + i*vec[1]
            print("b = ", b)
            self.maps[player_id, b[0], b[1]] = 1

    def check_intersection(self):
        for i in range(len(self.boats_set)):
            for j in range(i+1, len(self.boats_set)):
                if len(self.boats_list[i].cells.intersection(self.boats_list[j].cells)) != 0:
                    return False
                
        return True

    def place_random_boat(self, player_id):
        print("Inter", self.check_intersection())
        while not self.check_intersection():
            for s in self.boats_set:
                s.set_random()
                print(s.cells)

            print("----------")

        for s in self.boats_set:
            for cell in s.get_cells():
                self.maps[player_id, cell[0], cell[1]] = 1

    def shoot(self, player, co):
        player_id = self.players.index(player)
        opp_id = (~player_id) + 2
        hit = self.maps[opp_id, co[0], co[1]]
        print("Hit : ", hit)

        if hit:  # CIBLE TOUCHE
            self.serv.send(b"\x04\x01%c%c" % (co), self.players)
        else:  # COULER
            self.serv.send(b"\x04\x00%c%c" % (co), self.players)

        print("-> ", hasattr(self, "ai"))
        if hasattr(self, "ai"):
            fired = self.ai.fire()
            print("Fired : ", fired)

            while self.maps[player_id, fired[0], fired[1]]:
                self.serv.send(b"\x04\x01%c%c" % (fired), self.players)
                fired = self.ai.fire()

            self.serv.send(b"\x04\x00%c%c" % (fired), self.players)

    def run(self):
        pass

    def __repr__(self):
        return str(self.maps)
