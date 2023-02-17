import numpy as np
import random

class NeuralNetwork:
    """
    Idea for Neutral Network:
    We have giant neural network which calulates which areas is most significant to move.
    This represents the player's decision making.

    Then, we have a small neural network for all of the small which decide which direction to move and
    how many blobs to split and move.

    The small network will have an input set of the big net's output + 2 for blob coordinates.

    Both neural network weights are subject to genetic algorithm.
    """

    def __init__(self, input_length, hidden_length, layer_count, output_length):
        self.input_length = input_length
        self.hidden = []
        if (layer_count > 0):
            for layer in range(layer_count + 1):
                if layer == 0:
                    self.hidden.append(np.zeros((hidden_length, input_length)))
                elif layer == layer_count:
                    self.hidden.append(np.zeros((output_length, hidden_length)))
                else:
                    self.hidden.append(np.zeros((hidden_length, hidden_length)))
        else:
            self.hidden.append(np.zeros((output_length, input_length)))
        self.output_length = output_length

    def randomize_weight(self):
        """
        Randomize every weight of the neural network
        """
        for layer in range(len(self.hidden)):
            for x in range(len(self.hidden[layer])):
                for y in range(len(self.hidden[layer][x])):
                    self.set_weight(layer, x, y, random.random())


    def set_weight(self, layer, x, y, value):
        """
        Set a weight in a particular layer with a given value
        Argument: layer: specify which matrix
                  x: the row of the weight matrix
                  y: the column of the weight matrix
                  value: the weight to be set to
        """
        self.hidden[layer][x][y] = value