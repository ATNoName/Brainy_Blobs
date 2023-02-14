from __future__ import annotations
import random
import genetic as gene
import neural_network as nn
import player as p
import copy
import dcp


class Movement:
    def __init__(self, owner, initial_location: list[int], blob_number: int, target_location: list[int]):
        self.owner = owner
        self.initial_location = initial_location
        self.blob_number = blob_number
        self.target_location = target_location
    
    def process_collision(self, other: Movement) -> None:
        """ Sets blob numbers of movements to result after collision
        Args: other: other Movement to process collision with
        """
        if self.blob_number == other.blob_number:
            self.blob_number = 0
            other.blob_number = 0
        elif self.blob_number > other.blob_number:
            self.blob_number -= other.blob_number
            other.blob_number = 0
        else:
            self.blob_number = 0
            other.blob_number -= self.blob_number
            

class Board:
    # Note: the action should be simultaneous
    def __init__(self, length: int, width: int) -> None:
        self.board_state = list(list(Space() * length)) * width
        self.player_list = list()
        self.length = length
        self.width = width
        self.turn_counter = 0
    
    def get_space_at(self, location: list[int])  -> Space:
        """
        Args: location[]: = [x, y] for location on board_state
        Return: Space: Space at location
        """
        return self.board_state[location[0]][location[1]]

    def process_movement(self, initial_location_list: list[list[int]] = [], blob_number_list: list[int] = [], target_location_list: list[list[int]] = []) -> None:
        """
        Process all inputs from players from make_decisions. The index of
        the argument make up the input for the player
        Arguments: blob_location_list[]: the initial location of the blobs the player will move
        blob_number_list[]: the number of blobs the player will move
        target_list[]: the target location of the blobs.
        """
        unprocessed_movements = [Movement(self.get_space_at(initial_location_list[i]).get_owner(), 
                                          initial_location_list[i], 
                                          blob_number_list[i], 
                                          target_location_list[i]) for i in range(len(initial_location_list))]
        # Remove all blobs that are moving from space
        for movement in unprocessed_movements:
            start_space = self.get_space_at(movement.initial_location)
            start_space.add_number(-movement.blob_number)
        
        # Process all movement collisions (collisions where two groups of blobs move towards each other)
        self.process_movement_collisions(unprocessed_movements)
        
        # Process area collisions for movements with same owners, record collisions with different owners in lists
        self.process_area_collisions(unprocessed_movements)
        
        # now that all collisions are processed, execute movements
        for movement in unprocessed_movements:
            target_space = self.get_space_at(movement.target_location)
            if target_space.get_owner() == None:
                target_space.set_owner(movement.owner)
                target_space.set_number(movement.blob_number)
            elif target_space.get_owner() == movement.owner:
                target_space.add_number(movement.blob_number)
            else:
                if movement.blob_number > target_space.get_number():
                    self.conquer_space(self, movement.owner, target_space)
                target_space.set_number(abs(movement.blob_number - target_space.get_number())
        
        # Process encirclement
        self.process_encirclement()
    
    def process_movement_collisions(self, unprocessed_movements: list[Movement]) -> None:
        """
        Simplify the movements list so that there are no more collisions where two groups of blobs move towards each other
        Args: unprocessed_movements: movements list to be simplified
        """
        # Compare for each unique pair of indices in unprocessed movements
        for i in range(len(unprocessed_movements)):
            movement_i = unprocessed_movements[i]
            for j in range(i + 1, len(unprocessed_movements)):
                movement_j = unprocessed_movements[j]
                # if movement collision between movements
                if movement_i.initial_location == movement_j.target_location and movement_j.initial_location == movement_i.target_location:
                    movement_i.process_collision(movement_j)
        # delete processed movements (movements with blob_number of 0) from unprocessed_movements
        for index in sorted([i for i, x in enumerate(unprocessed_movements) if x.blob_number == 0], reverse=True):
            del unprocessed_movements[index]
    
    def process_area_collisions(self, unprocessed_movements: list[Movement]) -> None:
        """
        Simplify the movements list so that there are no more collisions where two groups of blobs meet at a space
        Args: unprocessed_movements: movements list to be simplified
        """
        collision_movements = []
        collision_targets = []
        for i in range(len(unprocessed_movements)):
            movement_i = unprocessed_movements[i]
            for j in range(i + 1, len(unprocessed_movements)):
                movement_j = unprocessed_movements[j]
                if movement_i.target_location == movement_j.target_location:
                    if movement_i.owner == movement_j.owner:
                        movement_i.blob_number += movement_j.blob_number
                        movement_j.blob_number = 0
                    else:
                        target = movement_i.target_location
                        if target not in collision_targets:
                            collision_targets.append(target)
                            collision_movements.append([])
                        idx = collision_targets.index(target)
                        for movement in [movement_i, movement_j]:
                            if movement not in collision_movements[idx]:
                                collision_movements[idx].append(movement)
        
        # Process area collisions between movements with different owners
        for i in range(len(collision_targets)):
            collision_movements[i].sort(key=lambda movement: movement.blob_number)
            n = len(collision_movements)
            result_blob_number = collision_movements[i].blob_number[n - 1] - collision_movements[i].blob_number[n - 2]
            if result_blob_number > 0:
                n -= 1
                collision_movements[i].blob_number[n - 1] = result_blob_number
            for j in range(n):
                collision_movements[i][j].blob_number = 0
        # delete processed movements (movements with blob_number of 0) from unprocessed_movements
        for index in sorted([i for i, x in enumerate(unprocessed_movements) if x.blob_number == 0], reverse=True):
            del unprocessed_movements[index]
    
    def conquer_space(self, owner: p.Player, space: Space) -> None:
        """
        Process space conquest which just set the space owner to the conquering player
        If the space has an opposing base, that base is deleted and player elimination is processed
        Argument: owner: the owner of the attacking blob
        x: the x coordinate of the space
        y: the y coordinate of the space
        """
        if space.get_type() == 1:
            self.delete_player(space.get_owner())
            space.set_type(0)
            # replace the deleted player with a new one
            bignet, smallnet = gene.fitness(owner, self)
            new_player = self.generate_base(1,2)
            new_player.set_ann(bignet, smallnet)
        space.set_owner(owner)

    def delete_player(self, player: p.Player):
        """
        Search for all player-owner blobs and delete them.
        Also search for player-owned space and revert them to neutral territory
        Remove player from list at the end
        Argument: player: the player marked for deletion
        """
        for space_column in self.board_state:
            for space in self.board_state[x]:
                if space.get_owner() == player:
                    space.set_owner(None)
                    space.set_number(0)
        self.player_list.pop(player)
    
    def position_encircled(self, position: list[int]) -> None | p.Player:
        """
        Args: position: position of space on board
        Return: None | p.Player: encircled by p.Player, None if not encircled
        """
        position_owner = self.get_space_at(position)
        prev_adjacent_owner = None
        for i in (0, 1):
            for j in (-1, 1):
                try:
                    adjacent_space = self.get_space_at([position[0] + i*j, position[1] + (not i)*j])
                    if adjacent_space.get_owner() == None or adjacent_space.get_number() == 0:
                        return None
                    if prev_adjacent_owner == None:
                        if adjacent_space.get_owner() != position_owner:
                            prev_adjacent_owner = adjacent_space.get_owner()
                        else:
                            return None
                    elif prev_adjacent_owner != adjacent_space.get_owner():
                        return None
                    else:
                        prev_adjacent_owner = adjacent_space.get_owner()
                except IndexError:
                    pass
                
        return prev_adjacent_owner
        
                                        
    def process_encirclement(self):
        """
        This function process the encirclement mechanic check which is
        2-4 blobs "surround" a blob army thus killing them without losing anything.
        """
        # Corners and edges require less square to occupy
        # Process: mark all encircled squares, then process the encirclement
        # Square with a base should be ignored
        for x in range(self.length):
            for y in range(self.width):
                space = self.get_space_at([x, y])
                if space.type != 1:
                    encircling_player = self.position_encircled([x, y])
                    if encircling_player != None:
                        space.set_owner(encircling_player)
                        space.set_number(0)


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
        self.type = 0   # 0 = empty space, 1 = base space
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
