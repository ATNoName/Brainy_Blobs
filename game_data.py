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
    
    def move_blob(self, blob_location, blob_number, target):
        # process blob movement
        pass
    
    def conquer_space(self, owner, x, y):
        # Note: base elimination is included in this
        pass

    def delete_player(self, player):
        # Search for all player-owner blobs and delete them. Remove player from list at the end
        pass

    def process_collision(self, blob1=0, blob2=0, blob3=0, blob4=0):
        # process blob collision
        if (blob1 > blob2 and blob1 > blob3 and blob1 > blob4):
            return blob1 - math.max(blob2, blob3, blob4)
        elif (blob2 > blob1 and blob2 > blob3 and blob2 > blob4):
            return blob2 - math.max(blob1, blob3, blob4)
        elif (blob3 > blob1 and blob3 > blob2 and blob3 > blob4):
            return blob3 - math.max(blob1, blob2, blob4)
        elif (blob4 > blob1 and blob4 > blob2 and blob4 > blob3):
            return blob4 - math.max(blob1, blob2, blob3)
        else:
            return 0

    def merge_blob(self, blob1=0, blob2=0, blob3=0, blob4=0):
        # process blob merge
        return blob1 + blob2
    
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
    
    def blob_income(self):
        # Give each base an extra blob
        pass

    def print_output(self):
        # Convert board state into data which can be processed and displayed.
        pass

class Space:
    def __init__(self):
        self.owner = None # Basically specify if base or blob army or none
        self.type = None
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