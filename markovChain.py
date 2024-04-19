# markovChain.py

import random
from itertools import product

class MarkovChain:
    def __init__(self, board):
        self.board = board

    def simulate_game(self, num_simulations):
        wins = {(d1, d2): [0, 0] for d1, d2 in product(range(1, 7), repeat=2)}

        for _ in range(num_simulations):
            board_copy = self.board.copy()

            while not board_copy.is_game_over():
                d1, d2 = board_copy.roll_dice()
                legal_moves = board_copy.get_legal_moves(board_copy.current_player, (d1, d2))
                if not legal_moves:
                    board_copy.current_player = 1 - board_copy.current_player
                    continue
                move = random.choice(legal_moves)
                board_copy.move_piece(board_copy.current_player, move[0], move[1])
                board_copy.current_player = 1 - board_copy.current_player

            winner = 0 if board_copy.borne_off[0] == 15 else 1
            wins[(d1, d2)][winner] += 1

        return wins

    def calculate_win_probability(self):
        num_simulations = 100000
        wins = self.simulate_game(num_simulations)

        win_probabilities = {}
        for dice_roll, win_counts in wins.items():
            total_wins = win_counts[0] + win_counts[1]
            if total_wins > 0:
                win_probabilities[dice_roll] = win_counts[0] / total_wins

        return win_probabilities

