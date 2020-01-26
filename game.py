
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

    def check_cell(x, y):
        adj_cells = 0
        for elements in directions:
            try:
                if board[x + elements[0], y + elements[1]] == 1:
                    adj_cells += 1
            except:
                pass
        return adj_cells

    for rows in range(50):
        for columns in range(50):
            adj_cells = check_cell(rows, columns)
            if board[rows, columns] == 1:
                if adj_cells > 3 or adj_cells < 2:
                    board[rows, columns] = 0
            else:
                if adj_cells == 3:
                    board[rows, columns] = 1
    return board
