# simulation.py

import random
from board import Board

def monte_carlo_simulation(num_simulations):
    wins = [0, 0] # Number of wins for each player

    for _ in range(num_simulations):
        board = Board()
        
        for x in range(100):
            d1,d2 = board.roll_dice()
            print(d1,d2)
            legal_moves = board.get_legal_moves(board.current_player, (d1,d2))
            print(legal_moves)
            if not legal_moves:
                board.current_player = 1 - board.current_player
                continue
            move = random.choice(legal_moves)
            print("selected move:", move)
            board.move_piece(board.current_player, move[0], move[1])
            print(board.is_game_over())
            board.current_player = 1 - board.current_player
        
        board.display_board_state()

        """
        while not board.is_game_over():
            board.display_board_state()
            d1, d2 = board.roll_dice()
            legal_moves = board.get_legal_moves(board.current_player, (d1, d2))
            move = random.choice(legal_moves)
            board.move_piece(board.current_player, move[0], move[1])
            board.current_player = 1 - board.current_player

        winner = 0 if board.borne_off[0] == 15 else 1
        wins[winner] += 1
        """

    return wins

num_simulations = 1
results = monte_carlo_simulation(num_simulations)

print("Player 1 wins:", results[0])
print("Player 2 wins:", results[1])