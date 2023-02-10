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
        pass

    def set_weight(self, layer, weight_array):
        pass

    def evaluate_ann(self):
        output_set = np.array()
        return output_set