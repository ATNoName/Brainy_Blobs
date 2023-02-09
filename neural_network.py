import random
import game_data

# Get all inputs for the player before implement ANN

class Player:
    def __init__(self, id, colour=(0,0,0), x=-1, y=-1):
        self.id = id
        self.colour = colour
        self.baseX = x
        self.baseY = y
        self.blob_location = list((x,y))
    
    def move_blob(self):
        # This function takes in a list and move the blob according to the list
        # I should eventually add in Enums for signify where to move
        pass

class NeuralNetwork:
    def __init__(self):
        pass