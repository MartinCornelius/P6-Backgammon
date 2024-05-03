import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from board import Board

def get_possible_starting_moves(dice, initial_board):
    boards = []
    init_board = Board(initial_board)
    if dice[0] != dice[1]:
        for d in dice:
            d2 = dice[0] if d == dice[1] else dice[1]

            first_move_board = init_board.copy()

            legal_moves = init_board.get_legal_moves(first_move_board.current_player, d)
            for move in legal_moves:
                first_move_board.move_piece(first_move_board.current_player, move[0], move[1])

                second_move_board = first_move_board.copy()
                legal_moves2 = second_move_board.get_legal_moves(second_move_board.current_player, d2)
                for move2 in legal_moves2:
                    second_move_board.move_piece(second_move_board.current_player, move2[0], move2[1])
                    boards.append(second_move_board.copy())
            
    else:
        d = dice[0]
        first_moves = init_board.get_legal_moves(init_board.current_player, d)
        first_boards = []
        for move1 in first_moves:
            temp_board = init_board.copy()
            temp_board.move_piece(temp_board.current_player, move1[0], move1[1])
            first_boards.append(temp_board)
        second_boards = []
        for board in first_boards:
            second_moves = board.get_legal_moves(board.current_player, d)
            for move2 in second_moves:
                temp_board = board.copy()
                temp_board.move_piece(temp_board.current_player, move2[0], move2[1])
                second_boards.append(temp_board)
        third_boards = []
        for board in second_boards:
            third_moves = board.get_legal_moves(board.current_player, d)
            for move3 in third_moves:
                temp_board = board.copy()
                temp_board.move_piece(temp_board.current_player, move3[0], move3[1])
                third_boards.append(temp_board)
        fourth_boards = []
        for board in third_boards:
            fourth_moves = board.get_legal_moves(board.current_player, d)
            for move4 in fourth_moves:
                temp_board = board.copy()
                temp_board.move_piece(temp_board.current_player, move4[0], move4[1])
                fourth_boards.append(temp_board)
        print(len(fourth_boards))


        
        """d = dice[0]
        temp_boards = []
        move_list = []

        first_move_board = init_board.copy()

        legal_moves = first_move_board.get_legal_moves(first_move_board.current_player, d)
        print("Lmoves: ", legal_moves)
        for move in legal_moves:

            second_move_board = first_move_board.copy()
            legal_moves2 = second_move_board.get_legal_moves(second_move_board.current_player, d)
            print("Lmoves2: ", legal_moves2)
            for move2 in legal_moves2:
                second_move_board.move_piece(second_move_board.current_player, move2[0], move2[1])

                third_move_board = second_move_board.copy()
                legal_moves3 = third_move_board.get_legal_moves(third_move_board.current_player, d)
                print("Lmoves3: ", legal_moves3)
                for move3 in legal_moves3:
                    third_move_board.move_piece(third_move_board.current_player, move3[0], move3[1])
                    
                    
                    fourth_move_board = third_move_board.copy()
                    legal_moves4 = fourth_move_board.get_legal_moves(fourth_move_board.current_player, d)
                    print("Lmoves4: ", legal_moves4)
                    for move4 in legal_moves4:
                        fourth_move_board.move_piece(fourth_move_board.current_player, move4[0], move4[1])
                        boards.append(fourth_move_board.copy())"""
    

    print("_______________________________________________")
    for board in boards:
        print(board.points[0])
    print("_______________________________________________")
    
    return boards

def monte_carlo_simulation(num_simulations, dice, initial_board = None):
    boards = get_possible_starting_moves(dice, initial_board)
    for board in boards:
        print(board.points)
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
            "points": [[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "bar": [0, 2],
            "borne_off": [0, 13],
            "current_player": 0
        }

results = monte_carlo_simulation(num_simulations, [1, 1], initial_board)
print(f"{len(results)} different starting moves")
for result in results:
    print(f"Player 1 winrate: {100*(result[0]/num_simulations)}%")
"""
# Plotting results
players = ['Player 1', 'Player 2']
percent_wins = [results[0] / num_simulations * 100, results[1] / num_simulations * 100]

df = pd.DataFrame({'Player': players, 'Win Percentage': percent_wins})
df.plot(kind='bar', x='Player', y='Win Percentage', color=['blue', 'green'])
plt.title('Win Percentage by Player')
plt.ylabel('Win Percentage')
plt.xlabel('Player')
plt.ylim(0, 100)
plt.show()
"""