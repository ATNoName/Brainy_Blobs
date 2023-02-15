import game_data as gd
import player as p
"""
import PIL
import numpy as np
import cv2
import glob
"""
import pygame as pg


def exampleBoard() -> gd.Board:
    board = gd.Board(8, 8)
    board.generate_base(4, 7)


def circle(surface, pos, r, fill, stroke):
    pg.gfxdraw.filled_circle(surface, pos[0], pos[1], r, fill)
    pg.gfxdraw.aacircle(surface, pos[0], pos[1], r, stroke)
    

def draw_normal_space(surface, window_size, board, cellposition: list[int], line_colour: tuple[int], colour: tuple[int]):
    midpoint = [cellposition[0]*window_size[0] / board.width, cellposition[1]*window_size[1] / board.length]
    cell_width = window_size[0] / board.width
    cell_length = window_size[1] / board.length
    circle_radius = min((cell_width, cell_length)) * 0.75
    circle(surface, midpoint, circle_radius, colour, line_colour)


def rect(surface, top_left, width_height, fill, stroke):
    pg.gfxdraw.box(surface, pg.Rect(top_left, width_height), fill)
    pg.gfxdraw.rectangle(surface, pg.Rect(top_left, width_height), stroke)


def draw_base_space(surface, window_size, board, cellposition: list[int], line_colour: tuple[int], colour: tuple[int]):
    midpoint = [cellposition[0]*window_size[0] / board.width, cellposition[1]*window_size[1] / board.length]
    cell_width = window_size[0] / board.width
    cell_length = window_size[1] / board.length
    rect_size = min((cell_width, cell_length)) * 0.75
    top_left = [midpoint[0]-rect_size*0.5, midpoint[1]-rect_size*0.5]
    width_height = [rect_size, rect_size]
    rect(surface, top_left, width_height, colour, line_colour)


def drawboard(surface: pg.Surface, window_size: tuple[int], board: gd.Board, line_colour):
    # draw grid lines
    for i in range(1, board.width + 1):
        pg.draw.line(surface, line_colour, [i*window_size[0] / board.width, 0], [i*window_size[0] / board.width, window_size[1]])
    for i in range(1, board.length + 1):
        pg.draw.line(surface, line_colour, [0, i*window_size[1] / board.length], [window_size[0], i*window_size[1] / board.length])
    # draw spaces
    for x in range(board.width):
        for y in range(board.height):
            cellposition = [x, y]
            space = board.get_space_at(cellposition)
            if space.get_type() == 0:
                draw_normal_space(surface, window_size, board, cellposition, line_colour, space.get_owner().get_colour())
            else:
                draw_base_space(surface, window_size, board, cellposition, line_colour, space.get_owner().get_colour())


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
