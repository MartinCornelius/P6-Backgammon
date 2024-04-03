# simulation.py

import random
from board import Board

def monte_carlo_simulation(num_simulations):
    wins = [0, 0] # Number of wins for each player

    for _ in range(num_simulations):
        board = Board()
        
        while not board.is_game_over():
            d1, d2 = board.roll_dice()
            legal_moves = board.get_legal_moves(board.current_player, (d1, d2))
            if not legal_moves:
                board.current_player = 1 - board.current_player
                continue
            move = random.choice(legal_moves)
            board.move_piece(board.current_player, move[0], move[1])
            board.current_player = 1 - board.current_player

        winner = 0 if board.borne_off[0] == 15 else 1
        wins[winner] += 1

    board.display_board_state()
    return wins

num_simulations = 10000 
results = monte_carlo_simulation(num_simulations)

print("Player 1 wins:", results[0])
print("Player 2 wins:", results[1])