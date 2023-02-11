from bifrost import dcp
import neutral_network as nn
import player
import game_data as gd
# implement dcp here

def dcp_activate(board = gd.Board()):
    player_list = board.player_list
    job = dcp.compute_for(player_list, dcp_ann)
    job.requires('numpy')
    job.compute_groups = [{'joinKey': 'test', 'joinSecret': 'dcp'}]
    job.public['name'] = "ANN evalutation via DCP!"
    return job.exec()


def dcp_ann(player, board = gd.Board()):
    import numpy as np
    player.generate_input_set(board)
    return player.make_decision()

