import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from board import Board

def is_duplicate(board, b):
    if board.current_player != b.current_player:
        return False
    if board.bar[0] != b.bar[0] or board.bar[1] != b.bar[1]:
        return False
    if board.borne_off[0] != b.borne_off[0] or board.borne_off[1] != b.borne_off[1]:
        return False
    for i in range(0,len(board.points[0])):
        if board.points[0][i] != b.points[0][i]:
            return False
        if board.points[1][i] != b.points[1][i]:
            return False
    return True

def get_possible_starting_moves(dice, initial_board):
    boards = []
    init_board = Board(initial_board)
    if dice[0] != dice[1]:
        for d in dice:
            d2 = dice[0] if d == dice[1] else dice[1]

            first_moves = init_board.get_legal_moves(init_board.current_player, d)
            first_boards = []
            for move in first_moves:
                temp_board = init_board.copy()
                temp_board.move_piece(temp_board.current_player, move[0], move[1])
                is_dup = False
                for b in first_boards:
                    if is_duplicate(temp_board, b):
                        is_dup = True
                if is_dup == False:
                    first_boards.append(temp_board)
            for board in first_boards:
                second_moves = board.get_legal_moves(board.current_player, d2)
                for move2 in second_moves:
                    temp_board = board.copy()
                    temp_board.move_piece(board.current_player, move2[0], move2[1])
                    is_dup = False
                    for b in boards:
                        if is_duplicate(temp_board, b):
                            is_dup = True
                    if is_dup == False:
                        boards.append(temp_board)
            
    else:
        d = dice[0]
        first_moves = init_board.get_legal_moves(init_board.current_player, d)
        first_boards = []
        for move1 in first_moves:
            temp_board = init_board.copy()
            temp_board.move_piece(temp_board.current_player, move1[0], move1[1])
            is_dup = False
            for b in first_boards:
                if is_duplicate(temp_board, b):
                    is_dup = True
            if is_dup == False:
                first_boards.append(temp_board)
        second_boards = []
        for board in first_boards:
            second_moves = board.get_legal_moves(board.current_player, d)
            for move2 in second_moves:
                temp_board = board.copy()
                temp_board.move_piece(temp_board.current_player, move2[0], move2[1])
                is_dup = False
                for b in second_boards:
                    if is_duplicate(temp_board, b):
                        is_dup = True
                if is_dup == False:
                    second_boards.append(temp_board)
        third_boards = []
        for board in second_boards:
            third_moves = board.get_legal_moves(board.current_player, d)
            for move3 in third_moves:
                temp_board = board.copy()
                temp_board.move_piece(temp_board.current_player, move3[0], move3[1])
                is_dup = False
                for b in third_boards:
                    if is_duplicate(temp_board, b):
                        is_dup = True
                if is_dup == False:
                    third_boards.append(temp_board)
        for board in third_boards:
            fourth_moves = board.get_legal_moves(board.current_player, d)
            for move4 in fourth_moves:
                temp_board = board.copy()
                temp_board.move_piece(temp_board.current_player, move4[0], move4[1])
                is_dup = False
                for b in boards:
                    if is_duplicate(temp_board, b):
                        is_dup = True
                if is_dup == False:
                    boards.append(temp_board)
    
    return boards

def monte_carlo_simulation(num_simulations, dice, initial_board = None):
    boards = get_possible_starting_moves(dice, initial_board)
    wins = [] # list of player 1 and 2 wins for each opening move
    for index, curr_board in enumerate(boards):
        wins.append([0,0])

        for sim in range(num_simulations):
            if sim % 1000 == 0:
                print(f"Simulation {sim}")

            board = curr_board.copy()
            
            while not board.is_game_over():
                dice_list = board.roll_dice()
                blocked_dice_list = []
                for _ in dice_list:
                    blocked_dice_list.append(False)
                while len(dice_list) > 0 and False in blocked_dice_list:
                    for i, d in enumerate(dice_list):    
                        legal_moves = board.get_legal_moves(board.current_player, d)

                        if not legal_moves:
                            blocked_dice_list[i] = True
                        else:
                            move = random.choice(legal_moves)
                            board.move_piece(board.current_player, move[0], move[1])

                            dice_list.remove(d)
                            blocked_dice_list = []
                            for _ in dice_list:
                                blocked_dice_list.append(False)

                board.current_player = 1 - board.current_player

            winner = 0 if board.borne_off[0] == 15 else 1
            wins[index][winner] += 1

    return wins

num_simulations = 1000

initial_board = {
            "points": [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "bar": [0, 1],
            "borne_off": [0, 14],
            "current_player": 0
        }

results = monte_carlo_simulation(num_simulations, [1, 1])
print(f"{len(results)} different starting moves")
biggest = 0
for i in range(len(results)):
    biggest = i if results[i][0] > results[biggest][0] else biggest
print(f"Player 1 highest winrate: {100*(results[biggest][0]/num_simulations)}% with move: {biggest}")

# Plotting results
moves = []
percent_wins = []
colors = []
for i in range(len(results)):
    moves.append(f"Move {i+1}")
    percent_wins.append(results[i][0] / num_simulations * 100)
    colors.append("magenta")

df = pd.DataFrame({'Move': moves, 'Win Percentage': percent_wins})
df.plot(kind='bar', x='Move', y='Win Percentage', color=colors)
plt.title('Win Percentage by Starting Move')
plt.ylabel('Win Percentage')
plt.xlabel('Starting move')
plt.ylim(0, 100)
plt.show()
