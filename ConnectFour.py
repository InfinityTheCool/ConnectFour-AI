"""
Author of Game Code: Keith Galli
Link: https://github.com/KeithGalli/Connect4-Python
Our group will use this Connect-4 program as a base to implement the AI agent.
We will make comments on the aspects of his code that we change and on the functions we implement

"""
import numpy as np
import pygame
import sys
import math
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

# Direction Tuples
# TOPLEFT, LEFT, BOTTOMLEFT, BOTTOM, BOTTOMRIGHT, RIGHT, TOPRIGHT
DIRECTIONLIST = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]


# This line of code is required in order for the program to run effectively given the recursive nature of the minmax
# function
sys.setrecursionlimit(5000)


"""
A method used to initialize the board
"""


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)
    return board


"""
A method to drop a piece at a given location on the board
"""


def drop_piece(board, row, col, piece):
    board[row][col] = piece


"""
A method used to check if a given column can have a chip placed in it
"""


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


"""
A method used to get the next open row available for a move in a given column 
"""


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


"""
A method used to print the board upright
"""


def print_board(board):
    print(np.flip(board, 0))


"""
This method was originally less than optimal using for loops to check the
win conditions. So we implemented an if-else structure to replace it
"""


def winning_move(testboard, col):
    y = col
    if get_next_open_row(testboard, col) is None:
        x = ROW_COUNT - 1
    else:
        x = get_next_open_row(testboard, col) - 1

    connectCount = 1
    # check for vertical win condition
    # Only need to check pieces lower than current row
    rTemp = x - 1
    if rTemp >= 0:
        if testboard[rTemp][y] == testboard[x][y]:
            connectCount += 1
            rTemp -= 1
            if rTemp >= 0:
                if testboard[rTemp][y] == testboard[x][y]:
                    connectCount += 1
                    rTemp -= 1
                    if rTemp >= 0:
                        if testboard[rTemp][y] == testboard[x][y]:
                            connectCount += 1

    if connectCount >= 4:
        return True

    # check for horizontal win condition
    connectCount = 1
    cTemp = y + 1
    if cTemp <= 6:
        if testboard[x][cTemp] == testboard[x][y]:
            connectCount += 1
            cTemp += 1
            if cTemp <= 6:
                if testboard[x][cTemp] == testboard[x][y]:
                    connectCount += 1
                    cTemp += 1
                    if cTemp <= 6:
                        if testboard[x][cTemp] == testboard[x][y]:
                            connectCount += 1

    cTemp = y - 1
    if cTemp >= 0:
        if testboard[x][cTemp] == testboard[x][y]:
            connectCount += 1
            cTemp -= 1
            if cTemp >= 0:
                if testboard[x][cTemp] == testboard[x][y]:
                    connectCount += 1
                    cTemp -= 1
                    if cTemp >= 0:
                        if testboard[x][cTemp] == testboard[x][y]:
                            connectCount += 1

    if connectCount >= 4:
        return True

    # check for positive diagonal win condition
    connectCount = 1
    rTemp = x - 1
    cTemp = y + 1
    if rTemp >= 0 and cTemp <= 6:
        if testboard[rTemp][cTemp] == testboard[x][y]:
            connectCount += 1
            cTemp += 1
            rTemp -= 1
            if rTemp >= 0 and cTemp <= 6:
                if testboard[rTemp][cTemp] == testboard[x][y]:
                    connectCount += 1
                    cTemp += 1
                    rTemp -= 1
                    if rTemp >= 0 and cTemp <= 6:
                        if testboard[rTemp][cTemp] == testboard[x][y]:
                            connectCount += 1

    rTemp = x + 1
    cTemp = y - 1
    if rTemp <= 5 and cTemp >= 0:
        if testboard[rTemp][cTemp] == testboard[x][y]:
            connectCount += 1
            cTemp -= 1
            rTemp += 1
            if rTemp <= 5 and cTemp >= 0:
                if testboard[rTemp][cTemp] == testboard[x][y]:
                    connectCount += 1
                    cTemp -= 1
                    rTemp += 1
                    if rTemp <= 5 and cTemp >= 0:
                        if testboard[rTemp][cTemp] == testboard[x][y]:
                            connectCount += 1
    if connectCount >= 4:
        return True

    # check for negative diagonal win condition
    connectCount = 1
    rTemp = x - 1
    cTemp = y - 1
    if rTemp >= 0 and cTemp >= 0:
        if testboard[rTemp][cTemp] == testboard[x][y]:
            connectCount += 1
            cTemp -= 1
            rTemp -= 1
            if rTemp >= 0 and cTemp >= 0:
                if testboard[rTemp][cTemp] == testboard[x][y]:
                    connectCount += 1
                    cTemp -= 1
                    rTemp -= 1
                    if rTemp >= 0 and cTemp >= 0:
                        if testboard[rTemp][cTemp] == testboard[x][y]:
                            connectCount += 1

    rTemp = x + 1
    cTemp = y + 1
    if rTemp <= 5 and cTemp <= 6:
        if testboard[rTemp][cTemp] == testboard[x][y]:
            connectCount += 1
            cTemp += 1
            rTemp += 1
            if rTemp <= 5 and cTemp <= 6:
                if testboard[rTemp][cTemp] == testboard[x][y]:
                    connectCount += 1
                    cTemp += 1
                    rTemp += 1
                    if rTemp <= 5 and cTemp <= 6:
                        if testboard[rTemp][cTemp] == testboard[x][y]:
                            connectCount += 1

    if connectCount >= 4:
        return True

    return False


"""
A method used to draw the board to the screen using pygame
"""


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


"""
This is a method used by our heuristic function to check the chips connected to any given location
"""


def checkChips(state, chip, type, direction):
    x, y = tuple(map(lambda i, j: i + j, chip, direction))
    num = 0

    for i in range(3):
        if 0 <= x <= 5 and 0 <= y <= 6:
            player = state[x][y]
            if type == player:
                num += 1
                x += direction[0]
                y += direction[1]
            else:
                break
    return num


"""
Our heuristic function, which is used to evaluate the board state at any given depth
"""


def heuristic_function(state, move, player):
    value = 0
    checkRow = get_next_open_row(state, move)
    if checkRow is None:
        x = ROW_COUNT - 1
    else:
        x = checkRow
    chip = (x, move)
    for direction in DIRECTIONLIST:
        value += checkChips(state, chip, player, direction)
    return value


"""
A method we created to copy a board state in order to pass it as a possible future move
"""


def generate_state(state, c, player):
    newstate = np.copy(state)
    r = get_next_open_row(newstate, c)
    newstate[r][c] = player
    return newstate


"""
Our alphabeta search, which returns the best move after evaluating future moves to a depth of 7
"""


def alphabeta_search(state):
    max_depth = 7

    infinity = 999999

    # Functions used by alphabeta
    def max_value(state, move, alpha, beta, depth):
        v = -infinity
        if winning_move(state, move):
            return v + depth
        if depth >= max_depth:
            return heuristic_function(state, move, 1)
        valid_col = []
        for i in range(0, COLUMN_COUNT):
            if is_valid_location(state, i):
                valid_col.append(i)
        for a in valid_col:
            v = max(v, min_value(generate_state(state, a, 2), a,
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, move, alpha, beta, depth):
        v = infinity
        if winning_move(state, move):
            return v + depth
        if depth >= max_depth:
            return heuristic_function(state, move, 2)
        valid_col = []
        for i in range(0, COLUMN_COUNT):
            if is_valid_location(state, i):
                valid_col.append(i)
        for a in valid_col:
            v = min(v, max_value(generate_state(state, a, 1), a,
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    valid_col = []
    for i in range(0, COLUMN_COUNT):
        if is_valid_location(board, i):
            valid_col.append(i)

    best_score = -infinity
    beta = infinity
    best_action = None
    choices = []
    for a in valid_col:
        v = min_value(generate_state(state, a, 2), a, best_score, beta, 1)
        choices.append((a, v))

    best_value = max(choices, key=lambda item: item[1])
    bests = [p for p in choices if best_value[1] == p[1]]
    if bests:
        (best_action, best_score) = random.choice(bests)
    return best_action


"""
This is the code used to initialize the board, open the window, and begin the game
"""

board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

"""
This game loop has been modified to incorporate an AI agent
replaces lines 270 to 325 of the original program
"""
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # this draws the chip moving on the columns
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn % 2 == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        # Ask for human player's turn
        if turn % 2 == 0:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, col):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                turn += 1
                print(board)
                print(turn)
                print_board(board)
                draw_board(board)

        # AI agents turn to make a move
        else:
            # Get best move from alphabeta search
            col = alphabeta_search(board)

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, col):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True
            print_board(board)
            draw_board(board)

            turn += 1

        if turn >= 42:
            label = myfont.render("It's a Tie!!", 1, BLUE)
            screen.blit(label, (40, 10))
            game_over = True

        if game_over:
            print("end")
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
