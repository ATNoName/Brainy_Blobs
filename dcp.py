from bifrost import dcp
import math
import neutral_network as nn
import player
import game_data as gd
# implement dcp here

def dcp_activate(board = gd.Board()):
    """
    Initalize DCP
    """
    player_list = board.player_list
    job = dcp.compute_for((player_list, board), dcp_ann)
    job.requires('numpy')
    job.compute_groups = [{'joinKey': 'test', 'joinSecret': 'dcp'}]
    job.public['name'] = "ANN evalutation via DCP!"
    result = job.exec()
    return result


def dcp_ann(player = player.Player(), board = gd.Board()):
    """
    Calculate player decision using other cores
    """
    import numpy as np
    player.generate_input_set(board)
    strat_set = player.make_decision()
    blob_location_list=[]
    blob_number_list=[]
    target_list=[]
    for coord in player.blob_list():
        input_set = strat_set
        input_set.append(coord[0] / board.length)
        input_set.append(coord[1] / board.width)
        player.smallnet.set_input(input_set)
        output_set = player.smallnet.evaluate_ann()
        output_set = output_set / np.linalg.norm(output_set)
        # Output set should be an array of 5 floating point which define
        # the percentage of what blobs move in which direction
        # The convention follows 0 = stay, 1-4 = Use value of direction enum
        # where highest percent goes first follow by second highest and etc
        blob = board.board_state[coord[0]][coord[1]].get_number()
        for i in range(1,5):
            size = math.round(board.board_state[coord[0]][coord[1]].get_number() * output_set[i])
            if (size != 0):
                loc, num, target = player.move_blob(player.Direction(i).name, size, coord[0], coord[1])
                blob_location_list.append(loc)
                blob_number_list.append(num)
                target_list.append(target)
                blob -= size
    return blob_location_list, blob_number_list, target_list
