import game_data as gd
import player as p
"""
import PIL
import numpy as np
import cv2
import glob
"""
import pygame as pg


def generateImage(board = gd.Board()):
    """
    This generator should have three phases
    1) create a new image canvas (as a matrix)
    2) colour the grid with colour provided in player object
    3) draw in the numbers (hardest part)
    """
    pg.init()
    bg_colour = pg.Color(230, 230, 230)
    line_colour = pg.Color(30, 30, 30)
    window_size = (800, 800)
    surface = pg.display.set_mode(window_size)

    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                break
        surface.fill(bg_colour)
        drawboard(surface, window_size, board, line_colour)
        pg.display.flip()

    pg.quit()


board = exampleBoard()
generateImage()
