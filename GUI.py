import numpy as np
import pygame as pg
from game import *
import tkinter
from tkinter import messagebox


class Grid:
    board = np.zeros((TILES, TILES), dtype=int)

    def __init__(self, rows, cols, width, height, state=0):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.state = state
        self.tiles = [[Tile(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

    def simulate(self):
        self.board = board_simulation(self.board)
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].set(self.board[i][j])

    def place(self, row, col, state):
        if self.tiles[row][col].value != state:
            self.tiles[row][col].set(state)
            self.board[row][col] = state
        else:
            self.tiles[row][col].set(0)
            self.board[row][col] = 0

    def draw(self, win):
        gap = int(self.width / TILES)
        thick = 1
        for i in range(self.rows + 1):
            pg.draw.line(win, BLACK, (0, i * gap), (self.width, i * gap), thick)
            pg.draw.line(win, BLACK, (i * gap, 0), (i * gap, self.height), thick)
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].draw(win)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / TILES
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def clear(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = 0
                self.tiles[i][j].set(0)


class Tile:
    rows = TILES
    cols = TILES

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def set(self, val):
        self.value = val

    def draw(self, win):
        gap = int(self.width / TILES)
        x = int(self.col * gap)
        y = int(self.row * gap)
        if self.value == 1:
            pg.draw.rect(win, BLACK, (x, y, gap, gap))
        elif self.value == 2:
            pg.draw.rect(win, BLUE, (x, y, gap, gap))
        elif self.value == 3:
            pg.draw.rect(win, GREEN, (x, y, gap, gap))


class Button:

    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, clicked=False):
        pg.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont('Noto Sans', 30, bold=False, italic=False)
        color = WHITE
        if clicked:
            color = RED
        text = font.render(self.text, 1, color)
        win.blit(text, (self.x + (int(self.width / 2) - int(text.get_width() / 2)),
                        self.y + (int(self.height / 2) - int(text.get_height() / 2))))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


class CellsButton(Button):
    def draw(self, win, clicked=1):
        color = BLACK
        if clicked == 2:
            color = BLUE
        elif clicked == 3:
            color = GREEN
        pg.draw.rect(win, color, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont('Noto Sans', 30, bold=False, italic=False)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x + (int(self.width / 2) - int(text.get_width() / 2)),
                        self.y + (int(self.height / 2) - int(text.get_height() / 2))))


def redraw_window(win, board, start_button, clear_button, color_button, simulate, state):
    win.fill(WHITE)
    if simulate:
        board.simulate()
        pg.time.wait(400)
    board.draw(win)
    start_button.draw(win, simulate)
    clear_button.draw(win)
    color_button.draw(win, state)


def main():
    win = pg.display.set_mode((WIDTH, HEIGHT + 80))
    pg.display.set_caption(TITLE)
    board = Grid(TILES, TILES, WIDTH, HEIGHT)
    start_button = Button(75, HEIGHT + 15, 100, 50, "Start")
    clear_button = Button(250, HEIGHT + 15, 100, 50, "Clear")
    color_button = CellsButton(425, HEIGHT + 15, 100, 50, "Color")
    icon = pg.image.load('src/bacteria.png')
    pg.display.set_icon(icon)
    simulate = False
    state = 1
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = board.click(pos)
                if clicked is not None:
                    board.place(clicked[0], clicked[1], state)
                if start_button.isOver(pos):
                    if simulate:
                        simulate = False
                    else:
                        simulate = True
                if clear_button.isOver(pos):
                    board.clear()
                if color_button.isOver(pos):
                    if state == 3:
                        state = 1
                    else:
                        state += 1

        redraw_window(win, board, start_button, clear_button, color_button, simulate, state)
        pg.display.update()


if __name__ == "__main__":
    if TILES <= 40 or TILES > 60:
        tkinter.Tk().wm_withdraw()
        tkinter.messagebox.showwarning("SETTINGS ERROR", "The tiles amount should be larger than 25 and lower than 60\n"
                                                         "Please change the settings")
        tkinter.Tk().withdraw()
    pg.init()
    main()
