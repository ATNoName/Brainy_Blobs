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
        action_processed = [False]*len(target_list)
        # Remove all blobs that are moving from space
        for i in range(len(target_list)):
            start_space = self.board_state[blob_location_list[i][0]][blob_location_list[i][1]]
            start_space.add_number(-blob_number_list[i])
        # Process all movement collisions
        for i in range(len(target_list)):
            if not action_processed[i]:
                # check if movementcollision needs to be processed
                if target_list[i] in blob_location_list:
                    target_index = blob_location_list.index(target_list[i])
                    if target_list[target_index] == blob_location_list[i]:
                        result = self.process_movementcollision(blob_number_list[i], blob_number_list[target_index])
                        if not result[0]:
                            blob_number_list[i] = 0
                            blob_number_list[target_index] = result[1]
                            action_processed[i] = True
                        else:
                            blob_number_list[i] = result[1]
                            blob_number_list[target_index] = 0
                            action_processed[target_index] = True
        # Process area collisions
        for i in range(len(target_list)):
            if not action_processed[i]:
            # check if areacollision needs to be processed
                blob_list = [blob_number_list[i]]
                blob_owner = [i]
                target_space = self.board_state[target_list[i][0]][target_list[i][1]]
                for j in range(i, len(target_list)):
                    if target_list[i] == target_list[j]:
                        blob_list.append(target_list[j])
                        blob_owner.append[j]
                if target_space.get_number() > 0:
                    blob_list.append(target_space.get_number())
                    blob_owner.append[-1]
                if len(blob_list) != 1:
                    result = self.process_areacollision(blob_list)
                    for player in blob_owner:
                        if result[0] != blob_owner[player]:
                            if blob_owner[player] >= 0:
                                action_processed[player] = True
                                blob_number_list[player] = 0
                            else:
                                target_space.set_number(0)
                        else:
                            blob_number_list = result[1]
        # Move any survivors to their target square and process any area conquest
        for i in range(len(target_list)):
            if not action_processed[i]:
                target_space = self.board_state[target_list[i][0]][target_list[i][1]]
                owner = self.board_state[blob_location_list[i][0]][blob_location_list[i][1]].get_owner()
                target_space.add_number(blob_number_list[i])
                if (target_space.get_owner() != owner):
                    self.conquer_space(owner, target_list[i][0], target_list[i][1])
                    target_space.add_number(-1)

        # Process encirclement
        self.process_encirclement()
    
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
        index = blob_list.index(first_max)
        blob_list[index] = 0
        second_max = max(blob_list)
        blob_list[index] = first_max
        if first_max == second_max:
            return None, 0
        return index, first_max - second_max

    def process_movementcollision(self, blob1, blob2):
        # this function is used for when two opposing blob
        # "hit" each other. Return True if atkowner won
        if (blob1 > blob2):
            return True, blob1 - blob2
        elif (blob2 > blob1):
            return False, blob2 - blob1
        else:
            return False, 0
    
    def process_encirclement(self):
        # This function is processed when a group of blob is "surrounded" by other blobs.
        # Corners and edges require less square to occupy
        # Process: mark all encircled squares, then process the encirclement
        # Square with a base should be ignored
        encircled = []
        for x in range(self.length):
            for y in range(self.width):
                space = self.board_state[x][y]
                if space.get_type() == 0:
                    neighbouring_square = []
                    if (not ((x + 1) == self.length)):
                        neighbouring_square.append(self.board_state[x+1][y])
                    if (not ((y + 1) == self.width)):
                        neighbouring_square.append(self.board_state[x][y+1])
                    if (not ((x -1) == -1)):
                        neighbouring_square.append(self.board_state[x-1][y])
                    if (not ((y -1) == -1)):
                        neighbouring_square.append(self.board_state[x][y-1])
                    # Condition:
                    # 1) check if neighbouring_square belong to same owner
                    # 2) check if neighbouring square oppose center owner
                    # 3) check if neighbouring_square has at least 1 blob
                    atkowner = neighbouring_square[0].get_owner()
                    if atkowner != space.get_owner():
                        is_encircled = True
                        for square in neighbouring_square:
                            if square.get_owner() != atkowner or square.get_number() == 0:
                                is_encircled = False
                        if is_encircled:
                            encircled.append((space, atkowner))
        # Eliminate the encirclement
        for square in encircled:
            square[0].set_number(0)
            square[0].set_owner(square[1])


    def generate_base(self, value, dist):
        # create new bases that are far away enough from others
        for self in range(value):
            is_suitable = False
            while (not is_suitable):
                is_suitable = True
                x = random.randint(0, self.length - 1)
                y = random.randint(0, self.width - 1)
                for player in self.player_list:
                    baseX, baseY = player.get_base()
                    if abs(baseX - x) + abs(baseY - y) < dist:
                        is_suitable = False
            player = player.Player(len(self.player_list), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), x, y)
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
