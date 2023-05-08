import random

class AI:
    """Class for the AI."""

    def __init__(self, boats: set):
        self.boats = list(boats)
        self.hit = []

    def place_boat(self, boat):
        # Generate a random position for the boat
        x = random.randint(1, 10)
        y = random.randint(1, 10)

        # Choose a random direction for the boat
        possible_directions = ['up', 'down', 'left', 'right']
        direction = random.choice(possible_directions)
        
        while not boat.fits_in_grid(x, y, direction):
            possible_directions.remove(direction)
            direction = random.choice(possible_directions)

        boat.place(x, y, direction)

        # Remove the boat from the list of boats
        self.boats.remove(boat)

    def fire(self):
        # Choose random position to fire that havn't been hit already
        x = random.randint(1, 10)
        y = random.randint(1, 10)