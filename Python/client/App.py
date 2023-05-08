from pygame import *
import tkinter.font as tkFont
from tkinter import *
from threading import Thread
from Battleship import BattleShip
class Server(Thread):
    def __init__(self, sock, host, port, app):
        Thread.__init__(self)
        self.sock = sock
        self.host = host
        self.port = port
        self.stop = False
        self.app : App = app
        self.battle = None
    def run(self):
        while not self.stop:
            msg,addr = self.sock.recvfrom(1024)
            print("recv msg from server",addr,"|",msg)

            match msg[0]:
                case 0: # NEW GAME CREATED
                    name = msg[1:]
                    self.app.new_game(name)
                case 1: # GAME STARTED
                    x = msg[1]
                    y = msg[2]
                    self.battle = BattleShip(x,y)
                    self.battle.start()
                case 2: # GAME ENDED
                    name = msg[1:]
                    pass
                case 3: # GAME ROOM UPDATE
                    is_waiting=msg[1]
                    len_name=msg[2]
                    name=msg[3:3+name_len]
    def send(self,o:bytes):
        self.sock.sendto(o, (self.host, self.port))
    

class App(Thread):
    """Class to represent the game application"""

    def __init__(self, server, host, port) -> None:
        Thread.__init__(self)
        self.root = Tk()
        self.serv = Server(server,host,port,self)

        self.root.title("Battleship")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.attributes("-fullscreen", True)

        self.in_menu = False
        
        self.serv.sock.sendto(b"Connected", (host, port))

        response = self.serv.sock.recvfrom(1024)
        
        if response[0] == b"\x00":
            # The user isn't known, show the connection screen
            """
            label = Label(root)
            ft = tkFont.Font(family="Times", size=20)
            label["font"] = ft
            label["justify"] = "center"
            label["text"] = "Username :"
            label.place(x=50, y=50, width=200, height=200)
            
            root.update()
            """

            self.text = Text(root)
            self.text.place(width=100, height=50, relx=0.0, rely=0.0, anchor='center')
            #self.text.place(x=50+label.winfo_width(), y=150, width=150, height=50)

            startButton = Button(root, text="Start", command=self.register_new_user)
            startButton.place(x=100, y=200, width=75, height=50)
        else:
            # The user is known, connect him directly
            print(f"Connected as {response[0].decode()}")
            self.menu(response[0].decode())
        self.serv.start()
    
    def run(self):
        self.root.mainloop()

    def register_new_user(self):
        toSend = b"\x02"
        self.username = self.text.get(0.1, END)[:-1]
        toSend += self.username.encode()

        self.serv.sock.sendto(toSend, (self.serv.host, self.serv.port))

        self.clear_widgets()

        self.root.update()

        self.menu(self.username)

    def menu(self, username):
        self.in_menu = True
        self.username = username
        # Username in top left corner
        label = Label(self.root, text=username)
        ft = tkFont.Font(family="Times", size=20)
        label["font"] = ft
        label["justify"] = "center"
        label.place(relx=0.0, rely=0.0)

        # List of current waiting rooms
        self.waiting_games = Listbox(self.root, width=30, height=10)
        self.waiting_games.place(relx=1, rely=0.5, anchor='center')

        # List of current games
        self.current_games = Listbox(self.root, width=30, height=10)
        self.current_games.place(relx=0.5, rely=0.5, anchor='center')

        # Sending request to get lists
        self.request_lists()

        # Adding games inside the list of waiting rooms
        for i in range(4):
            self.waiting_games.insert(END, f"Waiting Party {i+1}")
        
        # Adding games inside the list of current games
        for i in range(4):
            self.current_games.insert(END, f"Current Party {i+1}")

        # Button to create a new game
        newGameButton = Button(self.root, text="New Game", command=self.i_create_game)
        newGameButton.place(relx=0.5, rely=0.95, anchor='center')

    def new_game(self,author):
        if self.in_menu:
            self.waiting_games.insert(END, f"{author}'s game")

    def i_create_game(self):
        self.in_menu = False
        self.clear_widgets()

        # Party name in top center of the screen
        party_name = Label(self.root, text=f"{self.username}'s game", font=("Arial", 20))
        party_name.place(relx=0.45, rely=0.0)

        # List of players in the room
        self.players = Listbox(self.root, font=("Arial", 20), width=30, height=10)
        self.players.place(relx=0.5, rely=0.5, anchor='center')
        self.add_player(self.username)

        # Play against AI
        button_IA = Button(self.root, text="Play against AI", font=("Arial", 14), command= lambda: self.add_player("AI"))
        button_IA.place(relx=0.4, rely=0.95, anchor="center")

        # Start game
        self.button_start = Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game, state="disabled")
        self.button_start.place(relx=0.6, rely=0.95, anchor="center")
        create = b"\x00"
        self.serv.send(create)
    def start_game(self):
        start = b"\x03"
        #if self.players in "AI":
        if "AI" in self.players.get(0, END):
            start+=b"\x01"
        else:
            start+=b"\x00"
        self.serv.send(start)
    
    def add_player(self, username):
        self.players.insert(END, username)

        if self.players.size() == 2:
            self.button_start.configure(state="normal")

    def remove_player(self, username):
        index = self.players.get(0, END).index(username)
        self.players.delete(index)

        if self.players.size() < 2:
            self.button_start.configure(state="disabled")
        
    def join_game(self, party):
        # party = username
        toSend = b"\x01"
        toSend += party.encode()

        self.serv.send(toSend)

    def observe_game(self, party):
        toSend = b"\x04"
        toSend += party.encode()

        self.serv.send(toSend)

    def clear_widgets(self):
        for element in self.root.winfo_children():
            element.destroy()
            
        self.root.update()

    def request_lists(self):
        self.serv.send(b"\x05")