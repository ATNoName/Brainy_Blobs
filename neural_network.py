import numpy as np
import random

class NeuralNetwork:
    """
    Idea for Neutral Network:
    We have giant neural network which calulates which areas is most significant to move.
    This represents the player's decision making.

    Then, we have a small neural network for all of the small which decide which direction to move and
    how many blobs to split and move.

    Both neural network weights are subject to genetic algorithm.
    """

    def __init__(self, input_length, hidden_length, layer_count, output_length):
        self.input = np.zeros(input_length)
        self.hidden = []
        self.size = 0
        for layer in range(layer_count - 1):
            if layer == 0:
                self.hidden.append(np.zeros((hidden_length, input_length)))
                self.size += hidden_length*input_length
            elif layer == layer_count - 2:
                self.hidden.append(np.zeros((output_length, hidden_length)))
                self.size += hidden_length*output_length
            else:
                self.hidden.append(np.zeros((hidden_length, hidden_length)))
                self.size += hidden_length*hidden_length
        self.output = np.zeros(output_length)

    def randomize_weight(self):
        for layer in self.hidden:
            for x in self.hidden[layer]:
                for y in self.hidden[layer][x]:
                    self.set_weight(layer, x, y, random.random())


    def set_weight(self, layer, x, y, value):
        self.hidden[layer][x][y] = value

    def set_input(self, input = np.array()):
        self.input = input

    def evaluate_ann(self):
        self.output = self.input
        for i in range(0,len(self.hidden)):
            self.output = np.matmul(self.hidden[i], self.output)
        return self.output