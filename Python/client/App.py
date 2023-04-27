import socket

class App:
    """Class to represent the game application"""

    def __init__(self, root, server) -> None:
        root.title("Battleship")
        
        server.send(b"Connected")