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
    #b = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return b


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


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

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
# Calling function draw_board again
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

def evaluate(board, player, opponent):
    #check rows for win
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
            if board[1][col] == player:
                return 10
            elif board[1][col] == opponent:
                return -10
    # Check positive diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == board[r + 1][c + 1] and board[r + 1][c + 1] == board[r + 2][c + 2] and board[r + 2][c + 2] == board[r + 3][c + 3]:
                if board[r][c] == player:
                    return 10
                elif board[r][c] == opponent:
                    return -10

    # Check negative diaganols
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == board[r - 1][c + 1] and board[r - 1][c + 1] == board[r - 2][c + 2] and board[r - 2][c + 2] == board[r - 3][c + 3]:
                if board[r][c] == player:
                    return 10
                elif board[r][c] == opponent:
                    return -10
    return 0

@lru_cache
def minimax(board, depth, is_max, player, opponent):
    #
    m_board = []
    b = [board[i:i+COLUMN_COUNT] for i in range(0, len(board), COLUMN_COUNT)]
    t = []
    for s in b:
        for i in s:
            t.append(int(i))
        m_board.append(t)
        t = []

    print("m--------------")
    print_board(m_board)
    score = evaluate(m_board, player, opponent)
    if abs(score) == 10:
        return score
    if winning_move(m_board, player):
        return 0
    if is_max:
        best = -1000
        for col in range(COLUMN_COUNT):
            if is_valid_location(m_board, col):
                row = get_next_open_row(m_board, col)
                m_board[row-1][col-1] = player
                n_board = ""
                for r in range(ROW_COUNT):
                    for c in range(COLUMN_COUNT):
                        t = m_board[r][c]
                        n_board += str(t)
                best = max(best, minimax(n_board, depth+1, not is_max, player, opponent))
                m_board[row - 1][col - 1] = 0
        return best
    else:
        best = 1000
        for col in range(COLUMN_COUNT):
            if is_valid_location(m_board, col):
                row = get_next_open_row(m_board, col)
                m_board[row-1][col-1] = player
                n_board = ""
                for r in range(ROW_COUNT):
                    for c in range(COLUMN_COUNT):
                        t = m_board[r][c]
                        n_board += str(t)
                best = max(best, minimax(n_board, depth+1, not is_max, player, opponent))
                m_board[row - 1][col - 1] = 0
        return best

def computer_move(board, piece, oppon):
    global game_over
    best_val = -1000
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
                    m_board +=  t
            print("C--------------")
            print(m_board)
            move_val = minimax(m_board, 0, False, piece, oppon)
            board[row][col] = 0
            if move_val > best_val:
                best_move = (row, col)
                best_val = move_val
    drop_piece(board, best_move[0], best_val[1], piece)
    if winning_move(board, piece):
        label = myfont.render("Player " + piece + " wins!!", 1, (200, 9, 250))
        screen.blit(label, (40, 10))
        game_over = True


def main():
    global game_over, turn, board
    drop_piece(board, 0, 0, 2)
    drop_piece(board, 0, 1, 2)
    drop_piece(board, 0, 2, 2)
    print_board(board)
    draw_board(board)
    pygame.display.update()
    while not game_over:
        if turn == 0:
            computer_move(board, 1, 2)
        else:
            computer_move(board, 2, 1)
        print_board(board)
        draw_board(board)
        pygame.display.update()
        turn += 1
        turn = turn % 2
        if game_over:
            pygame.time.wait(3000)

            '''
   for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
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
                # # Ask for Player 2 Input
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)'''


if __name__ == "__main__":
    main()
