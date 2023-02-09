import random
import neural_network
import math

class Board:
    # Note: the action should be simulatenous
    def __init__(self, length, width):
        self.board_state = list(list(Space()*length))*width
        self.player_list = list()
        self.length = length
        self.width = width
        self.turn_counter = 0
    
    def process_movement(self, blob_location_list = [], blob_number_list= [], target_list = []):
        # process blob movement
        pass
    
    def conquer_space(self, owner, x, y):
        # Note: base elimination is included in this
        if (self.board_state[x][y].get_type() == 1):
            self.delete_player(self.board_state[x][y].get_owner())
            self.board_state[x][y].set_type(0)
        self.board_state.set_owner(owner)

    def delete_player(self, player):
        # Search for all player-owner blobs and delete them. Remove player from list at the end
        for x in self.board_state:
            for y in self.board_state[x]:
                if self.board_state[x][y].get_owner(player):
                    self.board_state.set_owner(None)
                    self.board_state.set_number(0)
        self.player_list.pop(player)

    def process_collision(self, blob_list = list()):
        # process blob collision
        first_max = max(blob_list)
        second_max = max(blob_list.pop(first_max))
        return first_max - second_max

    def merge_blob(self, blob_list = list()):
        # process blob merge
        merged_blob = 0
        for blob in blob_list:
            merged_blob += blob
        return merged_blob
    
    def complete_encirclement(self, length, width, reference_point):
        # definitely the hardest thing to program
        pass

    def generate_base(self, value):
        # create new bases (very primitive, replace if code is better)
        for self in range(value):
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.width - 1)
            player = neural_network.Player(len(self.player_list), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), x, y)
            self.board_state[x][y].set_type(1)
            self.board_state[x][y].set_number(10)
            self.board_state[x][y].set_owner(player)
            self.player_list.append(player, x, y)
    
    def blob_income(self, income):
        # Give each base an extra blob
        for player in self.player_list:
            x,y = player.get_base()
            self.board_state[x][y].set_number(self.board_state[x][y].get_number() + income)

    def generate_decision(self):
        # force all players to generate input for the board.
        # Output should be three list which process_movement can be executed
        pass

    def print_output(self):
        # Convert board state into data which can be processed and displayed.
        pass

class Space:
    def __init__(self):
        self.owner = None # Basically specify if base or blob army or none
        self.type = 0
        self.number = 0
    
    def get_owner(self):
        return self.owner

    def get_type(self):
        return self.type

    def get_number(self):
        return self.number
    
    def set_owner(self, owner):
        self.owner = owner

    def set_type(self, type):
        self.type = type

    def set_number(self, number):
        self.number = number