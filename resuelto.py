def is_solved(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return False
            if not is_valid(board, i, j, board[i][j]):
                return False
    return True

def input_value(board, row, col, value):
    if is_valid(board, row, col, value):
        board[row][col] = value
        return True
    else:
        return False
