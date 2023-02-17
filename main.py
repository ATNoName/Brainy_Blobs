import game_data as gd
import output
import distributive as dis

# This is for running the function

def generate_decision(self):
    """
    Force all players to generate input for the board.
    Output should be three list which process_movement can be executed
    """
    blob_list = []
    bignet_list = []
    smallnet_list = []
    input_list = []
    for player in self.player_list:
        blob_list.append(self.blob_search(player))
        bignet_list.append(player.bignet.hidden.tolist())
        smallnet_list.append(player.smallnet.hidden.tolist())
        input_list.append(self.generate_input_set(player).tolist())
    return dis.dcp_activate(blob_list, bignet_list, smallnet_list, input_list, self)

def main():
    population = 10
    length = 40
    width = 25
    frame_rate = 15 # how many image per second
    turn1 = frame_rate * 600 # how many turns for learning phase
    turn2 = frame_rate * 300 # how many turns for fighting phase
    turn3 = frame_rate * 300 # how many turns before the sim ends
    board = gd.Board(length, width)
    board.generate_base(population, 2)
    output.generateImage(board.print_output())
    for turn in range(turn1):
        blob_location_list, blob_number_list, target_list = board.generate_decision()
        board.process_movement(blob_location_list, blob_number_list, target_list)
        output.generateImage(board.print_output())
        board.blob_income(board.income)
        board.turn_counter += 1
    board.respawn = 0
    board.income = 5
    for turn in range(turn2):
        blob_location_list, blob_number_list, target_list = board.generate_decision()
        board.process_movement(blob_location_list, blob_number_list, target_list)
        output.generateImage(board.print_output())
        board.blob_income(board.income)
        board.turn_counter += 1
    board.income = 0
    for turn in range(turn3):
        blob_location_list, blob_number_list, target_list = board.generate_decision()
        board.process_movement(blob_location_list, blob_number_list, target_list)
        output.generateImage(board.print_output())
        board.blob_income(board.income)
        board.turn_counter += 1
        if (bool(blob_location_list)):
            break

def test():
    """
    Just test a function, edit this at own your accord
    """
    pass