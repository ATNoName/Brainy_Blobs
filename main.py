import game_data as gd
import output
import distributive as dis
import player as p
import pygame as pg

# This is for running the function

def generate_decision(board = gd.Board):
    """
    Force all players to generate input for the board.
    Output should be three list which process_movement can be executed
    """
    blob_list = []
    bignet_list = []
    smallnet_list = []
    input_list = []
    for player in board.player_list:
        blob_list.append(board.blob_search(player))
        bignet_list.append(player.bignet.hidden)
        smallnet_list.append(player.smallnet.hidden)
        input_list.append(board.generate_input_set(player))
    
    return dis.dcp_activate(blob_list, bignet_list, smallnet_list, input_list, board)

def main():
    population = 15
    length = 15
    width = 15
    frame_rate = 15 # how many image per second
    turn1 = frame_rate * 60 # how many turns for learning phase
    turn2 = frame_rate * 60 # how many turns for fighting phase
    turn3 = frame_rate * 30 # how many turns before the sim ends
    board = gd.Board(length, width)
    board.generate_base(population, 2)
    pg.init()
    window_size = (1280, 720)
    surface = pg.display.set_mode(window_size)
    output.generateImage(board.print_output(), surface, window_size)
    for turn in range(turn1):
        blob_location_list, blob_number_list, target_list = generate_decision(board)
        board.process_movement(blob_location_list, blob_number_list, target_list)
        output.generateImage(board.print_output(), surface, window_size)
        board.blob_income(board.income)
        board.turn_counter += 1
    board.respawn = 0
    board.income = 5
    for turn in range(turn2):
        blob_location_list, blob_number_list, target_list = generate_decision(board)
        board.process_movement(blob_location_list, blob_number_list, target_list)
        output.generateImage(board.print_output(), surface, window_size)
        board.blob_income(board.income)
        board.turn_counter += 1
    board.income = 0
    for turn in range(turn3):
        blob_location_list, blob_number_list, target_list = generate_decision(board)
        board.process_movement(blob_location_list, blob_number_list, target_list)
        output.generateImage(board.print_output(), surface, window_size)
        board.blob_income(board.income)
        board.turn_counter += 1
        if (bool(blob_location_list)):
            break
    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                break
    pg.quit()

def test():
    """
    Just test a function, edit this at own your accord
    """
    pass

main()
