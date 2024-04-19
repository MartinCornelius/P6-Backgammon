# simulation.py

import random
from board import Board
from markovChain import MarkovChain

def monte_carlo_simulation(num_simulations):
    wins = [0, 0] # Number of wins for each player

    for _ in range(num_simulations):
        if _ % 1000 == 0:
            print(f"Simulation {_}")

        init_state = {
            'points': [
                [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 5, 2, 1]
            ],
            'bar': [0,0],
            'borne_off': [0,0],
            'current_player': 0
        }
        board = Board(init_state)
        markov_chain = MarkovChain(board)
        win_probabilities = markov_chain.calculate_win_probability()
        print(win_probabilities)

        # best_roll = max(win_probabilities, key=win_probabilities.get)
        # d1, d2 = best_roll

    #     while not board.is_game_over():
    #         d1, d2 = board.roll_dice()
    #         legal_moves = board.get_legal_moves(board.current_player, (d1, d2))
    #         if not legal_moves:
    #             board.current_player = 1 - board.current_player
    #             continue
    #         move = random.choice(legal_moves)
    #         board.move_piece(board.current_player, move[0], move[1])
    #         board.current_player = 1 - board.current_player

    #     winner = 0 if board.borne_off[0] == 15 else 1
    #     wins[winner] += 1

    # return wins

num_simulations = 1
results = monte_carlo_simulation(num_simulations)

# print(f"Player 1 wins: {results[0]/num_simulations*100:.1f}% with {results[0]} games")
# print(f"Player 2 wins: {results[1]/num_simulations*100:.1f}% with {results[1]} games")
