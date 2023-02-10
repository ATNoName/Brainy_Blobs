import random
import neural_network as nn
import player
import copy


class Board:
    # Note: the action should be simultaneous
    def __init__(self, length, width):
        self.board_state = list(list(Space() * length)) * width
        self.player_list = list()
        self.length = length
        self.width = width
        self.turn_counter = 0

    def process_movement(self, blob_location_list=[], blob_number_list=[], target_list=[]):
        # process blob movement
        action_processed = [False] * len(target_list)

        for i in range(len(target_list)):
            if not action_processed[i]:
                # start the movement process
                action_processed[i] = True
                target_space = self.board_state[target_list[i][0]][target_list[i][1]]
                start_space = self.board_state[blob_location_list[i][0]][blob_location_list[i][1]]
                owner = start_space.get_owner()
                start_space.add_number(-blob_number_list[i])

                # check if movementcollision needs to be processed
                if target_list[i] in blob_location_list:
                    target_index = blob_location_list.index(target_list[i])
                    if target_list[target_index] == blob_location_list[i]:
                        result = self.process_movementcollision(blob_number_list[i], blob_number_list[target_index])
                        if not result[0]:
                            blob_number_list[i] = 0
                            blob_number_list[target_index] = result[1]
                            break
                        else:
                            blob_number_list[i] = result[1]

                # check if areacollision needs to be processed
                blob_list = [blob_number_list[i]]
                for j in range(i, len(target_list)):
                    if target_list[i] == target_list[j]:
                        blob_list.append(target_list[j])
                # move the damn thing

                # process area conquest

    def conquer_space(self, owner, x, y):
        # Note: base elimination is included in this
        if self.board_state[x][y].get_type() == 1:
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

    def process_areacollision(self, blob_list=list()):
        # process blob collision
        first_max = max(blob_list)
        second_max = max(blob_list.pop(first_max))
        return blob_list.index(first_max), first_max - second_max

    def process_movementcollision(self, blob1, blob2):
        # this function is used for when two opposing blob
        # "hit" each other. Return True if atkowner won
        if (blob1 > blob2):
            return True, blob1 - blob2
        elif (blob2 > blob1):
            return False, blob2 - blob1
        else:
            return False, 0

    def merge_blob(self, blob_list=list()):
        # process blob merge
        merged_blob = 0
        for blob in blob_list:
            merged_blob += blob
        return merged_blob

    def process_encirclement(self, point=(0, 0), atkowner=nn.Player()):
        # This function is processed when at least 4 blobs surrounds
        # one blob
        x, y = point
        self.board_state[x][y].set_number(0)
        self.board_state[x][y].set_owner(atkowner)
        self.board_state[x - 1][y].add_number(-1)
        self.board_state[x][y - 1].add_number(-1)
        self.board_state[x + 1][y].add_number(-1)
        self.board_state[x][y + 1].add_number(-1)

    def generate_base(self, value):
        # create new bases (very primitive, replace if code is better)
        for self in range(value):
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.width - 1)
            player = player.Player(len(self.player_list),
                                   (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), x, y)
            self.board_state[x][y].set_type(1)
            self.board_state[x][y].set_number(10)
            self.board_state[x][y].set_owner(player)
            self.player_list.append(player, x, y)

    def blob_income(self, income):
        # Give each base an extra blob
        for player in self.player_list:
            x, y = player.get_base()
            self.board_state[x][y].add_number(income)

    def generate_decision(self):
        # force all players to generate input for the board.
        # Output should be three list which process_movement can be executed
        pass

    def print_output(self):
        # Convert board state into data which can be processed and displayed.
        return copy.deepcopy(self.board_state)


class Space:
    def __init__(self):
        self.owner = None  # Basically specify if base or blob army or none
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

    def add_number(self, number):
        self.number += number
