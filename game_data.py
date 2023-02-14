import random
import genetic as gene
import neural_network as nn
import player as p
import copy
import dcp

class Board:
    # Note: the action should be simultaneous
    def __init__(self, length, width):
        self.board_state = list(list(Space() * length)) * width
        self.player_list = list()
        self.length = length
        self.width = width
        self.turn_counter = 0

    def process_movement(self, blob_location_list=[], blob_number_list=[], target_list=[]):
        """
        Process all inputs from players from make_decisions. The index of
        the argument make up the input for the player
        Arguments: blob_location_list[]: the initial location of the blobs
        blob_number_list[]: the number of blob that are going to move
        target_list[]: the target location of the blob.
        """
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
                blob_owner = [self.board_state[blob_location_list[i][0]][blob_location_list[i][1]].get_owner()]
                target_space = self.board_state[target_list[i][0]][target_list[i][1]]
                for j in range(i, len(target_list)):
                    if target_list[i] == target_list[j]:
                        # check if it belongs to any player and merge them and mark them as processed
                        isSame = False
                        owner_same = 0
                        for k in range(len(blob_owner)):
                            if self.board_state[blob_location_list[j][0]][blob_location_list[j][1]].get_owner() == blob_owner[k]:
                                isSame = True
                                owner_same = k
                                break
                        if isSame:
                            blob_list[owner_same] += blob_number_list[j]
                            blob_number_list[j] = 0
                            action_processed[j] = True
                        else:
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
                target_space.set_number(blob_number_list[i])
                if (target_space.get_owner() != owner):
                    self.conquer_space(owner, target_list[i][0], target_list[i][1])
                    target_space.add_number(-1)

        # Process encirclement
        self.process_encirclement()
    
    def conquer_space(self, owner, x, y):
        """
        Process space conquest which just set the space owner to the conquering player
        If the space has an opposing base, that base is deleted and player elimination is processed
        Argument: owner: the owner of the attacking blob
        x: the x coordinate of the space
        y: the y coordinate of the space
        """
        if self.board_state[x][y].get_type() == 1:
            self.delete_player(self.board_state[x][y].get_owner())
            self.board_state[x][y].set_type(0)
            bignet, smallnet = gene.fitness(owner, self)
            new_player = self.generate_base(1,2)
            new_player.set_ann(bignet, smallnet)
        self.board_state.set_owner(owner)

    def delete_player(self, player):
        """
        Search for all player-owner blobs and delete them.
        Also search for player-owned space and revert them to neutral territory
        Remove player from list at the end
        Argument: player: the player marked for deletion
        """
        for x in self.board_state:
            for y in self.board_state[x]:
                if self.board_state[x][y].get_owner(player):
                    self.board_state.set_owner(None)
                    self.board_state.set_number(0)
        self.player_list.pop(player)

    def process_areacollision(self, blob_list=list()):
        """
        Process area collision which is when opposing blob meet at the space
        Argument: blob_list: the list of blob that are going to be collided
        Return: index: the index of the blob who won
                first_max - second_max: the remaining blob after collision process
        """
        first_max = max(blob_list)
        index = blob_list.index(first_max)
        blob_list[index] = 0
        second_max = max(blob_list)
        blob_list[index] = first_max
        if first_max == second_max:
            return None, 0
        return index, first_max - second_max

    def process_movementcollision(self, blob1, blob2):
        """
        Process movement collision which is when opposing blobs have each
        other as targets
        Argument: blob1: the first blob army
                  blob2: the second blob army
        Return: winner: True if blob1 won and False if blob1 lost
                blob: the remaining blob after collision process
        """
        if (blob1 > blob2):
            return True, blob1 - blob2
        elif (blob2 > blob1):
            return False, blob2 - blob1
        else:
            return False, 0
    
    def process_encirclement(self):
        """
        This function process the encirclement mechanic check which is
        2-4 blobs "surround" a blob army thus killing them without losing anything.
        """
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
        """
        Generate new player and bases.
        Arguments: value: how many players and base will be added
                   dist: the minimum distance that base has to be from other to be valid
        """
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
            new_player = p.Player(len(self.player_list), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), x, y)
            self.board_state[x][y].set_type(1)
            self.board_state[x][y].set_number(10)
            self.board_state[x][y].set_owner(new_player)
            self.player_list.append(new_player)
            if value == 1:
                return new_player

    def blob_income(self, income):
        """
        Give each base extra blobs
        Argument: income: how many blobs to give
        """
        for player in self.player_list:
            x, y = player.get_base()
            self.board_state[x][y].add_number(income)

    def generate_decision(self):
        """
        Force all players to generate input for the board.
        Output should be three list which process_movement can be executed
        """
        return dcp.dcp_activate(self)

    def print_output(self):
        """
        Convert board state into data which can be processed and displayed
        by the output.py
        """
        return copy.deepcopy(self.board_state)


class Space:
    def __init__(self):
        self.owner = None  # Owner of the space, blob in that space are assumed to be part of the player
        self.type = 0   # Basically Specify if it is a base or empty space
        self.number = 0 # How many blob occupy the space

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
