import game_data as gd
# This is for running the function
def main():
    population = 1000
    length = 125
    width = 120
    frame_rate = 15 # how many image per second
    turn1 = frame_rate * 600 # how many turns for learning phase
    turn2 = frame_rate * 300 # how many turns for fighting phase
    turn3 = frame_rate * 300 # how many turns before the sim ends
    board = gd.Board()
    board.print_output()

def test():
    """
    Just test a function, edit this at own your accord
    """
    pass