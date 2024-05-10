import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from board import Board
import heuristics

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
                    temp_dice = dice_list.copy() # should delete duplicates
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
            "points": [[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "bar": [0, 1],
            "borne_off": [0, 14],
            "current_player": 0
        }

random_results, opening_moves1 = monte_carlo_simulation(num_simulations, [3, 4], None, heuristics.move_furthest_first)
furthest_results, opening_moves2 = monte_carlo_simulation(num_simulations, [3, 4], None, heuristics.move_furthest_first)
closest_results, opening_moves3 = monte_carlo_simulation(num_simulations, [3, 4], None, heuristics.move_furthest_first)
safe_results, opening_moves4 = monte_carlo_simulation(num_simulations, [3, 4], None, heuristics.keep_pieces_safe)
hit_results, opening_moves5 = monte_carlo_simulation(num_simulations, [3, 4], None, heuristics.hit_enemy_pieces)

print(f"num_simulations: {num_simulations}")

biggest = 0
for i in range(len(random_results)):
    biggest = i if random_results[i][0] > random_results[biggest][0] else biggest
print(f"Player 1 highest winrate random moves: {100*(random_results[biggest][0]/num_simulations)}% with move: {opening_moves1[biggest]}")
for i in range(len(furthest_results)):
    biggest = i if furthest_results[i][0] > furthest_results[biggest][0] else biggest
print(f"Player 1 highest winrate furthest moves: {100*(furthest_results[biggest][0]/num_simulations)}% with move: {opening_moves2[biggest]}")
for i in range(len(closest_results)):
    biggest = i if closest_results[i][0] > closest_results[biggest][0] else biggest
print(f"Player 1 highest winrate closest moves: {100*(closest_results[biggest][0]/num_simulations)}% with move: {opening_moves3[biggest]}")
for i in range(len(safe_results)):
    biggest = i if safe_results[i][0] > safe_results[biggest][0] else biggest
print(f"Player 1 highest winrate safe moves: {100*(safe_results[biggest][0]/num_simulations)}% with move: {opening_moves4[biggest]}")
for i in range(len(hit_results)):
    biggest = i if hit_results[i][0] > hit_results[biggest][0] else biggest
print(f"Player 1 highest winrate hit moves: {100*(hit_results[biggest][0]/num_simulations)}% with move: {opening_moves5[biggest]}")

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
plt.title('Win Percentage by Opening Move')
plt.ylabel('Win Percentage')
plt.xlabel('Opening Move')
plt.ylim(0, 100)
plt.show()
