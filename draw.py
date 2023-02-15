import random
"""
import PIL
import numpy as np
import cv2
import glob
"""
import pygame as pg
import pygame.gfxdraw as gfxdraw


def exampleBoard(width, height):
    #colours = [tuple([random.randint(0, 255) for i in range(3)]) for i in range(4)]
    colornames = ['LightCoral', 'DeepPink', 'Yellow', 'SpringGreen']
    colours = [pg.Color(name) for name in colornames]
    print(colours)
    board_data = [[[colours[random.randint(0, 3)], random.randint(0, 10), (not random.randint(0, width)) * 1, (not random.randint(0, 2)) * 1] for i in range(height)] for i in range(width)]
    for x in board_data:
        for y in x:
            if y[3] == 0:
                y[0] = pg.Color('White')
                y[1] = 0
                y[2] = 0
    return board_data


def circle(surface, pos, r, fill, stroke):
    """
    gfxdraw.filled_circle(surface, int(pos[0]), int(pos[1]), int(r), fill)
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), int(r), stroke)
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), int(r - 1), stroke)
    """
    gfxdraw.filled_circle(surface, int(pos[0]), int(pos[1]), int(r * 1.05), stroke)
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), int(r * 1.05), stroke)
    gfxdraw.filled_circle(surface, int(pos[0]), int(pos[1]), int(r * 0.95), fill)
    gfxdraw.aacircle(surface, int(pos[0]), int(pos[1]), int(r * 0.95), fill)
    

def draw_normal_space(surface, x, y, cell_width, cell_height, line_colour: tuple[int], colour: tuple[int]):
    midpoint = [x * cell_width + cell_width / 2, y * cell_height + cell_height / 2]
    circle_radius = min((cell_width, cell_height)) * 0.75 * 0.5
    circle(surface, midpoint, circle_radius, colour, line_colour)

def rect(surface, top_left, width_height, fill, stroke):
    pg.gfxdraw.box(surface, pg.Rect(top_left, width_height), stroke)
    pg.gfxdraw.box(surface, pg.Rect([top_left[0] + width_height[0] * 0.05, top_left[1] + width_height[1] * 0.05], [width_height[0] * 0.9, width_height[1] * 0.9]), fill)


def draw_base_space(surface, x, y, cell_width, cell_height, line_colour: tuple[int], colour: tuple[int]):
    midpoint = [x * cell_width + cell_width / 2, y * cell_height + cell_height / 2]
    rect_size = min((cell_width, cell_height)) * 0.75
    top_left = [midpoint[0]-rect_size*0.5, midpoint[1]-rect_size*0.5]
    width_height = [rect_size, rect_size]
    rect(surface, top_left, width_height, colour, line_colour)

def drawboard(surface: pg.Surface, window_size: tuple[int], board_data, line_colour, bg_colour):
    window_width = window_size[0]
    window_height = window_size[1]
    matrix_width = len(board_data)
    matrix_height = len(board_data[0])
    cell_width = window_width / matrix_width
    cell_height = window_height / matrix_height
    """
    # draw grid lines
    for i in range(1, matrix_width + 1):
        pg.draw.line(surface, line_colour, [i*cell_width, 0], [i*cell_width, window_height])
    for i in range(1, matrix_height + 1):
        pg.draw.line(surface, line_colour, [0, i*cell_height], [window_width, i*cell_height])
    """
    for i in range(matrix_width):
        top_left = [i*cell_width + cell_width / 2 - cell_width * 0.1, cell_height / 2]
        width_height = [cell_width * 0.2, window_height - cell_height]
        rect(surface, top_left, width_height, line_colour, line_colour)
    for i in range(matrix_height):
        top_left = [cell_width / 2, i*cell_height + cell_height / 2 - cell_height * 0.1]
        width_height = [window_width - cell_width, cell_height * 0.2]
        rect(surface, top_left, width_height, line_colour, line_colour)
    # draw spaces
    for x in range(matrix_width):
        for y in range(matrix_height):
            entry = board_data[x][y]
            colour = entry[0]
            number = entry[1]
            space_type = entry[2]
            if space_type == 0:
                draw_normal_space(surface, x, y, cell_width, cell_height, bg_colour, colour)
            else:
                draw_base_space(surface, x, y, cell_width, cell_height, bg_colour, colour)
            font = pg.font.Font(None, int(min(cell_width, cell_height) * 0.5))
            text = font.render(str(number), True, [255 - colour[i] for i in range(3)])
            text_rect = text.get_rect(center=(x * cell_width + cell_width / 2, y * cell_height + cell_height / 2))
            surface.blit(text, text_rect)


def generateImage():
    """
    This generator should have three phases
    1) create a new image canvas (as a matrix)
    2) colour the grid with colour provided in player object
    3) draw in the numbers (hardest part)
    """
    pg.init()
    bg_colour = pg.Color(230, 230, 230)
    line_colour = pg.Color('Indigo')
    window_size = (1920, 1080)
    surface = pg.display.set_mode(window_size)
    board_data = exampleBoard(40, 25)
    while True:
        for event in pg.event.get():
            if event == pg.QUIT:
                break
        surface.fill(bg_colour)
        drawboard(surface, window_size, board_data, line_colour, bg_colour)
        pg.display.flip()

    pg.quit()


if __name__ == "main":
    generateImage()
