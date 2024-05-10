import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from board import Board
import heuristics
import os
import datetime

def every_dice_simulation(num_simulations, initial_board = None, player_1_heuristic = heuristics.rand_choice, player_2_heuristic = heuristics.rand_choice):
    dice_pairs = []
    average_winrates = []
    highest_winrates = []
    best_moves = []
    for d1 in range(0 + 1, 6 + 1):
        for d2 in range(d1, 6 + 1):
            print(f"Running Monte Carlo with dice: ({d1}, {d2})")
            curr_wincounts, curr_moves = monte_carlo_simulation(num_simulations, [d1, d2], initial_board, player_1_heuristic = heuristics.rand_choice, player_2_heuristic = heuristics.rand_choice)
            sum = 0
            biggest = 0
            for i in range(len(curr_wincounts)):
                sum += curr_wincounts[i][0]
                if curr_wincounts[i][0] > curr_wincounts[biggest][0]:
                    biggest = i
            dice_pairs.append([d1, d2])
            average_winrates.append(100 * (sum / len(curr_wincounts)) / num_simulations)
            highest_winrates.append(100 * curr_wincounts[biggest][0] / num_simulations)
            best_moves.append(curr_moves[biggest])

    return dice_pairs, average_winrates, highest_winrates, best_moves

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
    # list of tuples: (board, moves_list)
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
                    if is_duplicate(temp_board, b[0]):
                        is_dup = True
                if is_dup == False:
                    first_boards.append((temp_board, [[move[0], move[1]]]))
            for board in first_boards:
                second_moves = board[0].get_legal_moves(board[0].current_player, d2)
                for move2 in second_moves:
                    temp_board = board[0].copy()
                    temp_board.move_piece(temp_board.current_player, move2[0], move2[1])
                    temp_board.current_player = 1 - temp_board.current_player
                    is_dup = False
                    for b in boards:
                        if is_duplicate(temp_board, b[0]):
                            is_dup = True
                    if is_dup == False:
                        temp_moves_list = board[1].copy()
                        temp_moves_list.append([move2[0], move2[1]])
                        boards.append((temp_board, temp_moves_list))
            
    else:
        d = dice[0]
        first_moves = init_board.get_legal_moves(init_board.current_player, d)
        first_boards = []
        for move1 in first_moves:
            temp_board = init_board.copy()
            temp_board.move_piece(temp_board.current_player, move1[0], move1[1])
            is_dup = False
            for b in first_boards:
                if is_duplicate(temp_board, b[0]):
                    is_dup = True
            if is_dup == False:
                first_boards.append((temp_board, [[move1[0], move1[1]]]))
        second_boards = []
        for board in first_boards:
            second_moves = board[0].get_legal_moves(board[0].current_player, d)
            for move2 in second_moves:
                temp_board = board[0].copy()
                temp_board.move_piece(temp_board.current_player, move2[0], move2[1])
                is_dup = False
                for b in second_boards:
                    if is_duplicate(temp_board, b[0]):
                        is_dup = True
                if is_dup == False:
                    temp_moves_list = board[1].copy()
                    temp_moves_list.append([move2[0], move2[1]])
                    second_boards.append((temp_board, temp_moves_list))
        third_boards = []
        for board in second_boards:
            third_moves = board[0].get_legal_moves(board[0].current_player, d)
            for move3 in third_moves:
                temp_board = board[0].copy()
                temp_board.move_piece(temp_board.current_player, move3[0], move3[1])
                is_dup = False
                for b in third_boards:
                    if is_duplicate(temp_board, b[0]):
                        is_dup = True
                if is_dup == False:
                    temp_moves_list = board[1].copy()
                    temp_moves_list.append([move3[0], move3[1]])
                    third_boards.append((temp_board, temp_moves_list))
        for board in third_boards:
            fourth_moves = board[0].get_legal_moves(board[0].current_player, d)
            for move4 in fourth_moves:
                temp_board = board[0].copy()
                temp_board.move_piece(temp_board.current_player, move4[0], move4[1])
                temp_board.current_player = 1 - temp_board.current_player
                is_dup = False
                for b in boards:
                    if is_duplicate(temp_board, b[0]):
                        is_dup = True
                if is_dup == False:
                    temp_moves_list = board[1].copy()
                    temp_moves_list.append([move4[0], move4[1]])
                    boards.append((temp_board, temp_moves_list))
    
    return boards

def monte_carlo_simulation(num_simulations, dice, initial_board = None, player_1_heuristic = heuristics.rand_choice, player_2_heuristic = heuristics.rand_choice):
    boards = get_possible_starting_moves(dice, initial_board)
    wins = [] # list of player 1 and 2 wins for each opening move
    first_moves = [] # list of src-dst moves to represent opening move
    for index, curr_board in enumerate(boards):
        wins.append([0,0])
        first_moves.append(curr_board[1])

        for sim in range(num_simulations):
            if sim % 1000 == 0:
                print(f"Simulation {sim}")

            board = curr_board[0].copy()
            
            while not board.is_game_over():
                dice_list = board.roll_dice()
                do_run = True
                while len(dice_list) > 0 and do_run:
                    temp_dice = [dice_list[0], dice_list[1]] if dice_list[0] != dice_list[1] else [dice_list[0]]
                    possible_moves = []
                    for d in temp_dice:    
                        legal_moves = board.get_legal_moves(board.current_player, d)

                        for move in legal_moves:
                            possible_moves.append([move[0], move[1], d])
                    
                    if len(possible_moves) == 0:
                        do_run = False
                    else:
                        if board.current_player == 0:
                            move = player_1_heuristic(possible_moves, board)
                        else:
                            move = player_2_heuristic(possible_moves, board)
                        board.move_piece(board.current_player, move[0], move[1])
                        dice_list.remove(move[2])
                            

                board.current_player = 1 - board.current_player

            winner = 0 if board.borne_off[0] == 15 else 1
            wins[index][winner] += 1

    return wins, first_moves

num_simulations = 10000

initial_board = {
            "points": [[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "bar": [0, 1],
            "borne_off": [13, 14],
            "current_player": 0
        }

biggest = 0
if not os.path.exists("logs"):
    os.mkdir("logs")
folder = f"logs/run{len(os.listdir('logs')) + 1}"
os.mkdir(folder)
print(f"num_simulations: {num_simulations}")

for heuristic in [heuristics.rand_choice, heuristics.move_furthest_first, heuristics.move_closest_first, heuristics.keep_pieces_safe, heuristics.hit_enemy_pieces]:
    start_time = datetime.datetime.now()
    dice_pairs, average_winrates, highest_winrates, best_moves = every_dice_simulation(num_simulations, None, heuristic)
    file = open(f"{folder}/{heuristic.__name__}.csv", "w")
    file.write("Dice Pair;Average Win%;Highest Win%;Best Move\n")
    for i in range(len(dice_pairs)):
        file.write(f"{dice_pairs[i]};{average_winrates[i]:.2f};{highest_winrates[i]:.2f};{best_moves[i]}\n")
    print(f"runtime of {heuristic.__name__}: {datetime.datetime.now() - start_time}")


# Plotting results
starting_dice = []
percent_wins = []
colors = []
for i in range(len(results)):
    starting_dice.append(f"[{dice_pairs[i][0]}, {dice_pairs[i][1]}]")
    percent_wins.append(results[i][0] / num_simulations * 100)
    colors.append("magenta")

df = pd.DataFrame({'Starting Roll': starting_dice, 'Win Percentage': percent_wins})
df.plot(kind='bar', x='Starting Roll', y='Win Percentage', color=colors)
plt.title('Highest Win Percentage by Starting Roll')
plt.ylabel('Win Percentage')
plt.xlabel('Starting Roll')
plt.ylim(0, 100)
plt.show()
