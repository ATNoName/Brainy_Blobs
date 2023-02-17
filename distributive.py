import math
import numpy as np
import player
import game_data as gd
# from bifrost import dcp
# implement dcp here

def dcp_activate(blob_list: list(), bignet_list: list(), smallnet_list: list(), input_list: list(), board: gd.Board):
    """
    Initalize DCP
    """
    result = []
    for i in range(len(blob_list)):
        result.append(dcp_ann(blob_list[i], bignet_list[i], smallnet_list[i], input_list[i], board.length, board.width))
    # job = dcp.compute_for((blob_list, bignet_list, smallnet_list, input_list, board.length, board.width), dcp_ann)
    # job.requires('numpy', 'math')
    # job.compute_groups = [{'joinKey': 'test', 'joinSecret': 'dcp'}]
    # job.public['name'] = "ANN evalutation via DCP!"
    # Should give us results in a 2d array of tuples where 1st dimension represent each player decision,
    # 2nd dimension represent the set of input for that player
    # result = job.exec(0.001)
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
                size = round(blob * small_output_set[i][j][k])
                if (size != 0):
                    loc, num, target = player_list[i].move_blob(player.Direction(k).name, size, blob_loc_list[i][j][0], blob_loc_list[i][j][1])
                    blob_location_list.append(loc)
                    blob_number_list.append(num)
                    target_list.append(target)
                    blob -= size
    return blob_location_list, blob_number_list, target_list

def dcp_ann(blob: list(), bignet: list(), smallnet: list(), input_set: list(), length: int(), width: int()):
    """
    Calculate player decision using other cores
    """
    # import numpy as np
    # import math
    # dcp.progress(0)
    # Unserialize the arguements
    blob_coord = blob
    np_bignet = np.array(bignet)
    np_smallnet = np.array(smallnet, dtype=object)
    np_input = np.array(input_set)
    bigoutput_set = np_input
    for i in range(0,len(np_bignet)):
        bigoutput_set = np.matmul(bigoutput_set, np_bignet[i])
    player_output = list()
    for player_blob in blob_coord:
        output_list = list()
        # dcp.progress(coord / len(player.blob_list()))
        np_input2 = np.copy(bigoutput_set)
        np_input2 = (np_input2 - np_input2.min()) / (np_input2.max() - np_input2.min())
        np_input2 = np.append(np_input2, [player_blob[0] / length])
        np_input2 = np.append(np_input2, [player_blob[1] / length])
        smalloutput_set = np.copy(np_input2)
        for i in range(0,len(np_smallnet)):
            smalloutput_set = np.matmul(np_smallnet[i], smalloutput_set)
        smalloutput_set = smalloutput_set / np.sum(smalloutput_set)
        player_output.append(smalloutput_set)
    # dcp.progress(100)
    return player_output
