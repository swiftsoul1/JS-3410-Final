# https://www.askpython.com/python/examples/connect-four-game
# taken 4/29/22
# changelog:
# - moved main to its own function
# - removed player input
# - created Computer_move, minimax, and evaluate functions to have the computer automate moves
# - in evaluate took the 'check diagonals' from winning_move and altered it to fit the context
import numpy as np
import pygame
import sys
import math
from functools import lru_cache
import random

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    b = []
    for r in range(ROW_COUNT):
        b.append([0] * COLUMN_COUNT)
    # b = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return b


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return -1


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True
    return False


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


board = create_board()
print_board(board)
game_over = False
turn = 0

# initalize pygame
pygame.init()

# define our screen size
SQUARESIZE = 100

# define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

MAX, MIN = 1000, -1000

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# Calling function draw_board again
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

nmtimes = 0;
def evaluate(board, player, opponent):
    # check rows for win
    for row in range(ROW_COUNT):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2] and board[row][2] == board[row][3]:
            if board[row][0] == player:
                return 10
            elif board[row][0] == opponent:
                return -10
        if board[row][1] == board[row][2] and board[row][2] == board[row][3] and board[row][3] == board[row][4]:
            if board[row][1] == player:
                return 10
            elif board[row][1] == opponent:
                return -10
        if board[row][2] == board[row][3] and board[row][3] == board[row][4] and board[row][4] == board[row][5]:
            if board[row][2] == player:
                return 10
            elif board[row][2] == opponent:
                return -10
        if board[row][3] == board[row][4] and board[row][4] == board[row][5] and board[row][5] == board[row][6]:
            if board[row][3] == player:
                return 10
            elif board[row][3] == opponent:
                return -10
    # check columns for win
    for col in range(COLUMN_COUNT):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col] and board[2][col] == board[3][col]:
            if board[0][col] == player:
                return 10
            elif board[0][col] == opponent:
                return -10
        if board[1][col] == board[2][col] and board[2][col] == board[3][col] and board[3][col] == board[4][col]:
            if board[1][col] == player:
                return 10
            elif board[1][col] == opponent:
                return -10
        if board[2][col] == board[3][col] and board[3][col] == board[4][col] and board[4][col] == board[5][col]:
            if board[2][col] == player:
                return 10
            elif board[2][col] == opponent:
                return -10
    # Check positive diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c + 1] and board[r + 1][c + 1] == board[r + 2][c + 2] and board[r + 2][
                c + 2] == board[r + 3][c + 3]:
                if board[r][c] == player:
                    return 10
                elif board[r][c] == opponent:
                    return -10

    # Check negative diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == board[r - 1][c + 1] and board[r - 1][c + 1] == board[r - 2][c + 2] and board[r - 2][
                c + 2] == board[r - 3][c + 3]:
                if board[r][c] == player:
                    return 10
                elif board[r][c] == opponent:
                    return -10
    return 0


@lru_cache
def minimax(board, depth, is_max, player, opponent, alpha, beta):
    global nmtimes
    nmtimes += 1

    print("m")
    m_board = []
    b = [board[i:i + COLUMN_COUNT] for i in range(0, len(board), COLUMN_COUNT)]
    t = []
    for s in b:
        for i in s:
            t.append(int(i))
        m_board.append(t)
        t = []
    score = evaluate(m_board, player, opponent)
    if winning_move(m_board, player):
        return 0
    if abs(score) == 10:
        return score

    if is_max:
        best = MIN
        for col in range(4):
            if is_valid_location(m_board, col):
                row = get_next_open_row(m_board, col)
                m_board[row][col] = player
                n_board = ""
                for r in range(ROW_COUNT):
                    for c in range(COLUMN_COUNT):
                        t = m_board[r][c]
                        n_board += str(t)
                val = minimax(n_board, depth + 1, not is_max, player, opponent, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                m_board[row][col] = 0
                if beta <= alpha:
                    return best
        if best == MIN:
            best = score
        return best
    else:
        best = MAX
        for col in range(4):
            if is_valid_location(m_board, col):
                row = get_next_open_row(m_board, col)
                m_board[row][col] = opponent
                n_board = ""
                for r in range(ROW_COUNT):
                    for c in range(COLUMN_COUNT):
                        t = m_board[r][c]
                        n_board += str(t)
                val = minimax(n_board, depth + 1, not is_max, player, opponent, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                m_board[row][col] = 0
                if beta <= alpha:
                    return best
        if best == MAX:
            best = score
        return best


def computer_move(board, piece, oppon):
    global game_over, screen, nmtimes
    best_val = MIN
    best_move = (-3, -3)
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            board[row][col] = piece
            m_board = ""
            for r in range(ROW_COUNT):
                for c in range(COLUMN_COUNT):
                    t = board[r][c]
                    t = str(t)
                    m_board += t

            move_val = minimax(m_board, 0, False, piece, oppon, MIN, MAX)
            print(move_val)
            board[row][col] = 0
            if move_val > best_val:
                best_move = (row, col)
                best_val = move_val
    nmtimes = 0
    print(best_move)
    drop_piece(board, best_move[0], best_move[1], piece)


# have it play the whole game ad display result
# run and change columns to see if works
# then add pruning 11.1
def main():
    global game_over, turn, board
    #print_board(board)
    draw_board(board)
    pygame.display.update()
    while not game_over:
        #print_board(board)
        draw_board(board)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #if event.type == pygame.KEYDOWN:
            if turn == 0:
                co = random.randint(1, 6)
                while get_next_open_row(board, co) == -1:
                    co = random.randint(1, 6)
                ro = get_next_open_row(board, co)
                drop_piece(board, ro, co, 1)
                draw_board(board)
                pygame.display.update()
                if winning_move(board, 1):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True


                # computer_move(board, 1, 2)
                turn += 1
                turn = turn % 2
            else:
                computer_move(board, 2, 1)
                if winning_move(board, 2):

                    label = myfont.render("Minimax  wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True
                turn += 1
                turn = turn % 2
                draw_board(board)
                pygame.display.update()

        if game_over:
            pygame.time.wait(3000)
            board = create_board()
            draw_board(board)
            pygame.display.update()
            game_over = False


def old_main():
    global game_over, turn, board
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    computer_move(board, 2, 1)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                # print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)
                    game_over = False
                    draw_board(board)
                    pygame.display.update()


if __name__ == "__main__":
    main()
