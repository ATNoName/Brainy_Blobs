import game_data as gd
import player as p
"""
import PIL
import numpy as np
import cv2
import glob
"""
import pygame as pg
import draw


def generateImage(board: gd.Board, surface: pg.Surface, window_size: tuple[int]):
    """
    This generator should have three phases
    1) create a new image canvas (as a matrix)
    2) colour the grid with colour provided in player object
    3) draw in the numbers (hardest part)
    """
    pg.init()
    bg_colour = pg.Color(230, 230, 230)
    line_colour = pg.Color('Indigo')
    surface.fill(bg_colour)
    board_data = [[] for i in range(board.width)]
    for x in range(board.width):
        for y in range(board.length):
            space = board.get_space_at([x, y])
            if space.get_owner() != None:
                board_data[x].append([space.get_owner().get_colour(), space.get_number(), space.get_type()])
            else:
                board_data[x].append([pg.Color('White'), 0, 0])
    draw.drawboard(surface, window_size, board_data, line_colour, bg_colour)
    pg.display.flip()
