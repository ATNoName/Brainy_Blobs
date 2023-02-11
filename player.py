import random
import enum
import numpy as np
import neutral_network as nn
from game_data import Board

# Get all inputs for the player before implement ANN

class Direction(enum):
    North = 1
    East = 2
    South = 3
    West = 4

class Player:
    def __init__(self, id, colour=(0,0,0), x=-1, y=-1, net = None):
        self.id = id
        self.colour = colour
        self.baseX = x
        self.baseY = y
        self.blob_location = list((x,y)) # location of all blobs
        if net is None:
            self.net = nn.NeuralNetwork(Board.length*Board.width, Board.length*Board.width, 3, Board.length*Board.width)
            self.net.randomize_weight()
        else:
            self.net = net

    def get_base(self):
        return (self.baseX, self.baseY)
    
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
    
    def generate_input_set(self, board = Board()):
        # generate input set for ANN
        pass

    def make_decision(self):
        # generate output by calling ANN evaluate
        pass