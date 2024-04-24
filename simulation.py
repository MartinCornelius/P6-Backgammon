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
            legal_moves = board.get_legal_moves(board.current_player, (d1, d2))
            if not legal_moves:
                board.current_player = 1 - board.current_player
                continue
            
            move1 = random.choice(legal_moves)
            board.move_piece(board.current_player, move1[0], move1[1])
            legal_moves.remove(move1)

            if legal_moves:
                move2 = random.choice(legal_moves)
                board.move_piece(board.current_player, move2[0], move2[1])

            board.current_player = 1 - board.current_player

        winner = 0 if board.borne_off[0] == 15 else 1
        wins[winner] += 1

    return wins

num_simulations = 1000
results = monte_carlo_simulation(num_simulations)

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
