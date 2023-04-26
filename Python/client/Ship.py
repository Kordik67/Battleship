class Ship:
    """Class to represent a ship"""
    
    def __init__(self, length) -> None:
        self.length = length
        self.hp = length
        self.position = () # (x, y, direction)