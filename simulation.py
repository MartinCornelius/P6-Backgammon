import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from board import Board

def monte_carlo_simulation(num_simulations):
    wins = [0, 0] # Number of wins for each player

    for sim in range(num_simulations):
        if sim % 1000 == 0:
            print(f"Simulation {sim}")

        board = Board()
        
        while not board.is_game_over():
            d1, d2 = board.roll_dice()
            legal_moves_d1 = board.get_legal_moves(board.current_player, d1)
            legal_moves_d2 = board.get_legal_moves(board.current_player, d2)

            if not legal_moves_d1 and not legal_moves_d2:
                board.current_player = 1 - board.current_player
                continue
            die = random.choice((1, 2))

            # gets the first move:
            if die == 1 and legal_moves_d1:
                move1 = random.choice(legal_moves_d1)
                board.move_piece(board.current_player, move1[0], move1[1])    
            elif die == 2 and legal_moves_d2:
                move1 = random.choice(legal_moves_d2)
                board.move_piece(board.current_player, move1[0], move1[1])
            # gets the other move:
            if die == 2:
                legal_moves_cont = board.get_legal_moves(board.current_player, d1)
            else:
                legal_moves_cont = board.get_legal_moves(board.current_player, d2)
            
            if legal_moves_cont:
                move2 = random.choice(legal_moves_cont)
                board.move_piece(board.current_player, move2[0], move2[1])
            # if the dice er equal do two more moves, if possible
            legal_moves_cont = board.get_legal_moves(board.current_player, d1)
            if legal_moves_cont and d1 == d2:
                move3 = random.choice(legal_moves_cont)
                board.move_piece(board.current_player, move3[0], move3[1])
                legal_moves_cont = board.get_legal_moves(board.current_player, d1)
                if legal_moves_cont and d1 == d2:
                    move4 = random.choice(legal_moves_cont)
                    board.move_piece(board.current_player, move4[0], move4[1])
            board.current_player = 1 - board.current_player
        board.display_board_state()
        print("\n")
        winner = 0 if board.borne_off[0] == 15 else 1
        wins[winner] += 1

    return wins

num_simulations = 100
results = monte_carlo_simulation(num_simulations)

# Plotting results
players = ['Player 1', 'Player 2']
percent_wins = [results[0] / num_simulations * 100, results[1] / num_simulations * 100]

print(percent_wins)

df = pd.DataFrame({'Player': players, 'Win Percentage': percent_wins})
df.plot(kind='bar', x='Player', y='Win Percentage', color=['blue', 'green'])
plt.title('Win Percentage by Player')
plt.ylabel('Win Percentage')
plt.xlabel('Player')
plt.ylim(0, 100)
plt.show()
