from bifrost import dcp
import math
import neural_network as nn
import player
import game_data as gd
# implement dcp here

def dcp_activate(board = gd.Board()):
    """
    Initalize DCP
    """
    player_list = board.player_list
    job = dcp.compute_for((player_list, board), dcp_ann)
    job.requires('numpy', 'math')
    job.compute_groups = [{'joinKey': 'test', 'joinSecret': 'dcp'}]
    job.public['name'] = "ANN evalutation via DCP!"
    # Should give us results in a 2d array of tuples where 1st dimension represent each player decision,
    # 2nd dimension represent the set of input for that player
    result = job.exec(0.001)
    blob_location_list=[]
    blob_number_list=[]
    target_list=[]
    for i in range(len(result)):
        for r in range(len(result[i])):
            blob_location_list.append(r[i][r][0])
            blob_number_list.append(r[i][r][1])
            target_list.append[r[i][r][2]]
    return blob_location_list, blob_number_list, target_list


def dcp_ann(player = player.Player(), board = gd.Board()):
    """
    Calculate player decision using other cores
    """
    import numpy as np
    import math
    dcp.progress(0)
    blob_list = board.blob_search(player)
    board.generate_input_set(player)
    strat_set = player.bignet.evaluate_ann()
    blob_location_list=[]
    blob_number_list=[]
    target_list=[]
    for coord in blob_list:
        dcp.progress(coord / len(player.blob_list()))
        input_set = strat_set
        input_set.append(coord[0] / board.length)
        input_set.append(coord[1] / board.width)
        player.smallnet.set_input(input_set)
        output_set = player.smallnet.evaluate_ann()
        output_set = output_set / np.sum(output_set)
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
    dcp.progress(100)
    return blob_location_list, blob_number_list, target_list
