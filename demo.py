def isDrawover():
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col]==2:
                return False
    return True