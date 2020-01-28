# game logic and board simulation
from settings import *


def board_simulation(board):
    directions = [[1, 0],
               [0, 1],
               [1, 1],
               [-1, 0],
               [0, -1],
               [-1, -1],
               [1, -1],
               [-1, 1]
               ]
    changes = {}

    def check_cell(x, y):
        adj_cells = 0
        for elements in directions:
            if 0 <= x + elements[0] <= TILES - 1 and 0 <= y + elements[1] <= TILES - 1:
                if board[x + elements[0], y + elements[1]] == 1:
                    adj_cells += 1

        return adj_cells

    for rows in range(TILES):
        for columns in range(TILES):
            adj_cells = check_cell(rows, columns)
            if board[rows, columns] == 1:
                if adj_cells > 3 or adj_cells < 2:
                    changes["{} {}".format(rows, columns)] = 0
            else:
                if adj_cells == 3:
                    changes["{} {}".format(rows, columns)] = 1
    for key, value in changes.items():
        x, y = map(int, key.split())
        board[x, y] = value
    return board
