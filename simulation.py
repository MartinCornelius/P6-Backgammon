from board import Board
import heuristics
import os
import datetime

def every_dice_simulation(num_simulations, initial_board = None, player_1_heuristic = heuristics.rand_choice, player_2_heuristic = heuristics.rand_choice):
    dice_pairs = []
    average_winrates = []
    highest_winrates = []
    best_moves = []
    average_borne_offs = []
    average_hits = []
    average_opponent_hits = []
    highest_hits = []
    for d1 in range(0 + 1, 6 + 1):
        for d2 in range(d1, 6 + 1):
            print(f"Running Monte Carlo with dice: ({d1}, {d2})")
            curr_wincounts, curr_moves, curr_borne_off, curr_hits, highest_hit = monte_carlo_simulation(num_simulations, [d1, d2], initial_board, player_1_heuristic, player_2_heuristic)
            win_sum = 0
            win_biggest = 0
            borne_off_sum = 0
            hits_sum = 0
            opponent_hits_sum = 0
            hits_biggest = 0
            for i in range(len(curr_wincounts)):
                win_sum += curr_wincounts[i][0]
                borne_off_sum += curr_borne_off[i][0]
                hits_sum += curr_hits[i][0]
                opponent_hits_sum += curr_hits[i][1]
                if curr_wincounts[i][0] > curr_wincounts[win_biggest][0]:
                    win_biggest = i
                if highest_hit[i] > highest_hit[hits_biggest]:
                    hits_biggest = i
            dice_pairs.append([d1, d2])
            average_winrates.append(100 * (win_sum / len(curr_wincounts)) / num_simulations)
            highest_winrates.append(100 * curr_wincounts[win_biggest][0] / num_simulations)
            best_moves.append(curr_moves[win_biggest])
            average_borne_offs.append((borne_off_sum / len(curr_borne_off)) / num_simulations)
            average_hits.append((hits_sum / len(curr_hits)) / num_simulations)
            average_opponent_hits.append((opponent_hits_sum / len(curr_hits)) / num_simulations)
            highest_hits.append(highest_hit[hits_biggest])

    return dice_pairs, average_winrates, highest_winrates, best_moves, average_borne_offs, average_hits, average_opponent_hits, highest_hits

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
    total_borne_off = [] # amount of pieces borne off for both players for each game
    total_hits = [] # total amount of hits for both players for each game
    first_moves = [] # list of src-dst moves to represent opening move
    highest_hit = []
    for index, curr_board in enumerate(boards):
        wins.append([0, 0])
        total_borne_off.append([0, 0])
        total_hits.append([0, 0])
        first_moves.append(curr_board[1])
        highest_hit.append(0)

        for sim in range(num_simulations):
            if sim % 1000 == 0:
                print(f"Simulation {sim}")
            tmp_hits = 0

            board = curr_board[0].copy()
            
            while not board.is_game_over():
                dice_list = board.roll_dice()
                do_run = True
                while len(dice_list) > 0 and do_run:
                    if len(dice_list) > 1:
                        temp_dice = [dice_list[0], dice_list[1]] if dice_list[0] != dice_list[1] else [dice_list[0]]
                    else:
                        temp_dice = dice_list
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
                        prev_bar = board.bar.copy()
                        board.move_piece(board.current_player, move[0], move[1])
                        if prev_bar[0] < board.bar[0]:
                            total_hits[index][1] += 1
                        elif prev_bar[1] < board.bar[1]:
                            total_hits[index][0] += 1
                            tmp_hits += 1
                        dice_list.remove(move[2])
                        
                board.current_player = 0 if board.current_player == 1 else 1

            winner = 0 if board.borne_off[0] == 15 else 1
            wins[index][winner] += 1
            total_borne_off[index][0] += board.borne_off[0]
            total_borne_off[index][1] += board.borne_off[1]
            highest_hit[index] = tmp_hits if highest_hit[index] < tmp_hits else highest_hit[index]

    return wins, first_moves, total_borne_off, total_hits, highest_hit

program_start_time = datetime.datetime.now()

num_simulations = 10000

running_game_board = {
            "points": [[0, 0, 0, 0, 0, 5, 2, 3, 2, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1, 2, 3, 2, 5, 0, 0, 0, 0, 0]],
            "bar": [0, 0],
            "borne_off": [0, 0],
            "current_player": 0
        }

far_home_board = {
            "points": [[0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0]],
            "bar": [0, 0],
            "borne_off": [0, 0],
            "current_player": 0
        }

near_home_board = {
            "points": [[5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5]],
            "bar": [0, 0],
            "borne_off": [0, 0],
            "current_player": 0
        }

even_home_board = {
            "points": [[2, 2, 3, 4, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 4, 3, 2, 2]],
            "bar": [0, 0],
            "borne_off": [0, 0],
            "current_player": 0
        }

biggest = 0
if not os.path.exists("logs"):
    os.mkdir("logs")
folder = f"logs/run{len(os.listdir('logs')) + 1}-sims{num_simulations}"
os.mkdir(folder)
print(f"num_simulations: {num_simulations}")

"""
heuristic_list = [heuristics.rand_choice, heuristics.move_furthest_first, heuristics.move_closest_first, heuristics.keep_pieces_safe, heuristics.hit_enemy_pieces]
for heuristic in heuristic_list:
    start_time = datetime.datetime.now()
    dice_pairs, average_winrates, highest_winrates, best_moves, average_borne_offs, average_hits, average_opponent_hits, highest_hits = every_dice_simulation(num_simulations, None, heuristic, heuristics.rand_choice)
    file = open(f"{folder}/{heuristic.__name__}.csv", "w")
    file.write("Dice Pair;Average Win%;Highest Win%;Best Move;Average Pieces Borne Off;Average Hits Made;Average Opponent Hits;Highest Amount Hits\n")
    for i in range(len(dice_pairs)):
        file.write(f"{dice_pairs[i]};{average_winrates[i]:.2f};{highest_winrates[i]:.2f};{best_moves[i]};{average_borne_offs[i]:.2f};{average_hits[i]:.2f};{average_opponent_hits[i]:.2f};{highest_hits[i]}\n")
    print(f"runtime of {heuristic.__name__}: {datetime.datetime.now() - start_time}")
"""

curr_wincounts, curr_moves, curr_borne_off, curr_hits, highest_hit = monte_carlo_simulation(num_simulations, [2, 2], None, heuristics.rand_choice, heuristics.rand_choice)

win_sum = 0
win_biggest = 0
borne_off_sum = 0
hits_sum = 0
opponent_hits_sum = 0
hits_biggest = 0
for i in range(len(curr_wincounts)):
    win_sum += curr_wincounts[i][0]
    borne_off_sum += curr_borne_off[i][0]
    hits_sum += curr_hits[i][0]
    opponent_hits_sum += curr_hits[i][1]
    if curr_wincounts[i][0] > curr_wincounts[win_biggest][0]:
        win_biggest = i
    if highest_hit[i] > highest_hit[hits_biggest]:
        hits_biggest = i

average_winrates = 100 * (win_sum / len(curr_wincounts)) / num_simulations
highest_winrates = 100 * curr_wincounts[win_biggest][0] / num_simulations
best_move = curr_moves[win_biggest]
average_borne_offs = (borne_off_sum / len(curr_borne_off)) / num_simulations
average_hits = (hits_sum / len(curr_hits)) / num_simulations
average_opponent_hits = (opponent_hits_sum / len(curr_hits)) / num_simulations
highest_hits = highest_hit[hits_biggest]

print(f"{average_winrates}, {highest_winrates}, {best_move}, {average_borne_offs}, {average_hits}, {average_opponent_hits}, {highest_hits}")

print(f"total runtime of program: {datetime.datetime.now() - program_start_time}")
