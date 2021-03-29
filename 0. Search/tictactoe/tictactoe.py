"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """ Returns starting state of the board. """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """ Returns player who has the next turn on a board. """

    x_o_count = 0
    for row in board:
        x_o_count = x_o_count + row.count(X) - row.count(O)
    if (x_o_count == 0):
        return X
    else:
        return O

def actions(board):
    """ Returns set of all possible actions (i, j) available on the board. """
    Set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                Set.add((i, j))
    return Set

def result(board, action):
    """ Returns the board that results from making move (i, j) on the board. """
    board_copy = [row.copy() for row in board]
    if (player(board_copy) == O):
        board_copy[action[0]][action[1]] = O
    else:
        board_copy[action[0]][action[1]] = X
    return board_copy


def winner(board):
    """ Returns the winner of the game, if there is one. """

    row1, row2, row3 = board

    if row1.count(X) == 3 or row2.count(X) == 3 or row3.count(X) == 3:
        return X
    elif row1.count(O) == 3 or row2.count(O) == 3 or row3.count(O) == 3:
        return O
    elif row1[0] == row2[0] == row3[0] == X or row1[1] == row2[1] == row3[1] == X or row1[2] == row2[2] == row3[2] == X:
        return X
    elif row1[0] == row2[0] == row3[0] == O or row1[1] == row2[1] == row3[1] == O or row1[2] == row2[2] == row3[2] == O:
        return O
    elif row1[0] == row2[1] == row3[2] and row1[0] is not None:
        return row1[0]
    elif row1[2] == row2[1] == row3[0] and row1[2] is not None:
        return row1[2]
    else:
        return None

def terminal(board):
    """ Returns True if game is over, False otherwise. """

    row1, row2, row3 = board
    if row1[0] is not None and row1.count(row1[0]) == 3:
        return True
    elif row2[0] is not None and row2.count(row2[0]) == 3:
        return True
    elif row3[0] is not None and row3.count(row3[0]) == 3:
        return True
    elif row1[0] == row2[0] == row3[0] and row1[0] is not None:
        return True
    elif row1[1] == row2[1] == row3[1] and row1[1] is not None:
        return True
    elif row1[2] == row2[2] == row3[2] and row1[2] is not None:
        return True
    elif row1[0] == row2[1] == row3[2] and row1[0] is not None:
        return True
    elif row1[2] == row2[1] == row3[0] and row1[2] is not None:
        return True
    elif row1.count(None) + row2.count(None) + row3.count(None) == 0:
        return True
    else:
        return False


def utility(board):
    """ Returns 1 if X has won the game, -1 if O has won, 0 otherwise. """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def best_action(board):
    """ Returns the optimal action for the current player on the board. """
    
    best_action = None
    if player(board) == X:
        best_value = -999

        for action in actions(board):
            value = minimax(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = 999

        for action in actions(board):
            value = minimax(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action

    return best_action

def minimax(board):
    if terminal(board):
        return utility(board)

    if player(board) == X:                  # Find max value
        best_value = -999        
        for action in actions(board):
            value = minimax(result(board, action))
            best_value = max(best_value, value)
        return best_value
    else:                                   # Find min value
        best_value = 999        
        for action in actions(board):
            value = minimax(result(board, action))
            best_value = min(best_value, value)
        return best_value