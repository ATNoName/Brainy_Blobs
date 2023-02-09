import random
import enum
import numpy as np
from game_data import Board

# Get all inputs for the player before implement ANN

class Direction(enum):
    North = 1
    East = 2
    South = 3
    West = 4

class Player:
    def __init__(self, id, colour=(0,0,0), x=-1, y=-1):
        self.id = id
        self.colour = colour
        self.baseX = x
        self.baseY = y
        self.blob_location = list((x,y)) # location of all blobs
    
    def move_blob(self, direction = Direction(), number=0, x=0, y=0):
        # return Input for board
        target = tuple()
        if direction == Direction.North:
            target = (x, y-1)
        elif direction == Direction.East:
            target = (x+1, y)
        elif direction == Direction.South:
            target = (x, y+1)
        else:
            target = (x-1,y)
        return ((x,y), number, target)

    def blob_search(self, board = Board()):
        # Get all blob location
        self.blob_location = list()
        for x in board.width:
            for y in board.length:
                if board.board_state.getowner() == self:
                    self.blob_location.append((x,y))
        return
    
    def make_decision(self):
        # use Neutral Network to generate input for board
        pass


class NeuralNetwork:
    """
    Idea for Neutral Network:
    We have giant neural network which calulates which areas is most significant.
    This represents the player's decision making.

    Then, we have a small neural network for all of the small which decide which direction to move and
    how many blobs to split and move.
    """

    def __init__(self):
        pass

    def calculate_neuron(self):
        pass

    def calculate_input(self, location = (0,0)):
        pass