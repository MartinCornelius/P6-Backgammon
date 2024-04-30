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
