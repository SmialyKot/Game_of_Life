from settings import *
import numpy as np
import pygame as pg
from game import *


class Grid:
    board = np.zeros((50, 50), dtype=int)

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.tiles = [[Tile(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]

    def update_model(self):
        self.model = [[self.tiles[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def simulate(self):
        self.board = board_simulation(self.board)
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].set(self.board[i][j])
        self.update_model()

    def place(self, row, col):
        if self.tiles[row][col].value == 0:
            self.tiles[row][col].set(1)
            self.board[row][col] = 1
        else:
            self.tiles[row][col].set(0)
            self.board[row][col] = 0
        self.update_model()

    def draw(self, win):
        gap = int(self.width / 50)
        for i in range(self.rows + 1):
            thick = 1
            pg.draw.line(win, BLACK, (0, i*gap), (self.width, i*gap), thick)
            pg.draw.line(win, BLACK, (i * gap, 0), (i * gap, self.height), thick)
        for i in range(self.rows):
            for j in range(self.cols):
                self.tiles[i][j].draw(win)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 50
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None


class Tile:
    rows = 50
    cols = 50

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height

    def set(self, val):
        self.value = val

    def draw(self, win):
        gap = int(self.width / 50)
        x = int(self.col * gap)
        y = int(self.row * gap)
        if self.value == 1:
            pg.draw.rect(win, BLACK, (x, y, gap, gap))
      
            
class Button:
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = "Start"
        
    def draw(self, win, clicked):
        pg.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height))
        font = pg.font.SysFont('Noto Sans', 30, bold=False, italic=False)
        color = WHITE
        if clicked:
            color = RED
        text = font.render(self.text, 1, color)
        win.blit(text, (self.x + (int(self.width/2) - int(text.get_width()/2)), self.y + (int(self.height/2) - int(text.get_height()/2))))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def redraw_window(win, board, start_button, simulate):
    win.fill(WHITE)
    if simulate:
        board.simulate()
        pg.time.wait(500)
    board.draw(win)
    start_button.draw(win, simulate)


def main():
    win = pg.display.set_mode((WIDTH, HEIGHT + 80))
    pg.display.set_caption(TITLE)
    board = Grid(50, 50, WIDTH, HEIGHT)
    start_button = Button(75, 815, 100, 50)
    icon = pg.image.load('src/bacteria.png')
    pg.display.set_icon(icon)
    simulate = False
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = board.click(pos)
                if clicked is not None:
                    board.place(clicked[0], clicked[1])
                if start_button.isOver(pos):
                    if simulate:
                        simulate = False
                    else:
                        simulate = True
        redraw_window(win, board, start_button, simulate)
        pg.display.update()


if __name__ == "__main__":
    pg.init()
    main()
