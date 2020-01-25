import numpy as np


def board_print(board):
    for rows in board:
        print(rows)


def board_simulation(board, gen):
    directions = [[1, 0],
               [0, 1],
               [1, 1],
               [-1, 0],
               [0, -1],
               [-1, -1],
               [1, -1],
               [-1, 1]
               ]

    def check_cell(x, y):
        adj_cells = 0
        for elements in directions:
            try:
                if board[x + elements[0], y + elements[1]] == 1:
                    adj_cells += 1
            except:
                pass
        return adj_cells

    for _ in range(gen):
        for rows in range(15):
            for columns in range(15):
                adj_cells = check_cell(rows, columns)
                if board[rows, columns] == 1:
                    if adj_cells > 3 or adj_cells < 2:
                        board[rows, columns] = 0
                else:
                    if adj_cells == 3:
                        board[rows, columns] = 1
    board_print(board)


if __name__ == "__main__":
    board = np.zeros((15, 15), dtype=int)
    print("Provide coordinates of live cells in format (x y (range 0-14)), when finished press enter:")
    while (x := input()) != "":
        # j == y, i == x
        i, j = map(int, x.split())
        board[j][i] = 1
    gen = int(input("Please specify which generation should be displayed:"))
    board_simulation(board, gen)
