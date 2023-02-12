import random
import enum
import numpy as np
import neutral_network as nn
import game_data

# Get all inputs for the player before implement ANN

class Direction(enum):
    North = 1
    East = 2
    South = 3
    West = 4

class Player:
    def __init__(self, id, colour=(0,0,0), x=-1, y=-1, length = 0, width = 0, net = nn.NeuralNetwork()):
        self.id = id
        self.colour = colour
        self.baseX = x
        self.baseY = y
        self.blob_location = list((x,y)) # location of all blobs
        if net is None:
            self.net = nn.NeuralNetwork(length*width, length*width, 3, length*width)
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

    def blob_search(self, board = game_data.Board()):
        # Get all blob location
        self.blob_location = list()
        for x in board.width:
            for y in board.length:
                if board.board_state.getowner() == self:
                    self.blob_location.append((x,y))
        return
    
    def generate_input_set(self, board = game_data.Board()):
        input_set = np.zeros(board.length*board.width)
        base_location = []
        for x in range(board.length):
            for y in range(board.width):
                """
                Idea here, area with high enemy blob have a high input value
                Wheras, area with high player blob have low input value
                Normalize the entire vector, divide by 2 and add 0.5
                This formula means that player controlled areas are <0.5 and
                enemy controlled areas are >0.5.
                Bases are forced to be set to 0 and 1.
                """
                if (board.board_state[x][y].get_type() == 0):
                    if (board.board_state[x][y].get_owner() == self):
                        input_set[x*board.length+y] = - board.board_state[x][y].get_number()
                    else:
                        input_set[x*board.length+y] = board.board_state[x][y].get_number()
                else:
                    base_location.append((x,y))
        input_set = input_set / np.linalg.norm(input_set)
        self.net.input = input_set

    def make_decision(self):
        # generate output by calling ANN evaluate
        return self.net.evaluate_ann()