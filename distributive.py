from bifrost import dcp
import math
import neural_network as nn
import player
import game_data as gd
# implement dcp here

def dcp_activate(blob_list: list(), bignet_list: list(), smallnet_list: list(), input_list: list(), board: gd.Board):
    """
    Initalize DCP
    """
    job = dcp.compute_for((blob_list, bignet_list, smallnet_list, input_list, board.length, board.width), dcp_ann)
    job.requires('numpy', 'math')
    job.compute_groups = [{'joinKey': 'test', 'joinSecret': 'dcp'}]
    job.public['name'] = "ANN evalutation via DCP!"
    # Should give us results in a 2d array of tuples where 1st dimension represent each player decision,
    # 2nd dimension represent the set of input for that player
    result = job.exec(0.001)
    return dcp_convert(result, board, blob_list)

def dcp_convert(small_output_set: list(), board: gd.Board, blob_loc_list: list()):
    blob_location_list=[]
    blob_number_list=[]
    target_list=[]
    player_list = board.player_list
    for i in range(len(player_list)):
        for j in range(len(small_output_set[i])):
            # Output set should be an array of 5 floating point which define
            # the percentage of what blobs move in which direction
            # The convention follows 0 = stay, 1-4 = Use value of direction enum
            # where highest percent goes first follow by second highest and etc
            loc = board.get_space_at(blob_loc_list[i][j])
            blob = loc.get_number()
            for k in range(1,5):
                size = math.round(blob * small_output_set[i][j][k])
                if (size != 0):
                    loc, num, target = player.move_blob(player.Direction(i).name, size, blob_loc_list[i][j][0], blob_loc_list[i][j][1])
                    blob_location_list.append(loc)
                    blob_number_list.append(num)
                    target_list.append(target)
                    blob -= size
    return blob_location_list, blob_number_list, target_list

def dcp_ann(blob: list(), bignet: list(), smallnet: list(), input_set: list(), length: int(), width: int()):
    """
    Calculate player decision using other cores
    """
    import numpy as np
    import math
    dcp.progress(0)
    # Unserialize the arguements
    blob_coord = blob
    np_bignet = np.array(bignet)
    np_smallnet = np.array(smallnet)
    np_input = np.array(input_set)
    bigoutput_set = np_input
    for i in range(0,len(np_bignet)):
        bigoutput_set = np.matmul(np_bignet[i], bigoutput_set)
    player_output = list()
    for player_blob in blob_coord:
        output_list = list()
        for coord in player_blob:
            dcp.progress(coord / len(player.blob_list()))
            np_input2 = np.copy(bigoutput_set)
            np_input2.append(coord[0] / length)
            np_input2.append(coord[1] / width)
            smalloutput_set = np.copy(bigoutput_set)
            for i in range(0,len(np_smallnet)):
                bigoutput_set = np.matmul(np_smallnet[i], bigoutput_set)
            smalloutput_set = smalloutput_set / np.sum(smalloutput_set)
            output_list.append(smalloutput_set)
        player_output.append(output_list)
    dcp.progress(100)
    return player_output
