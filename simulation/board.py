# board.py

import random

class Board:
    def __init__(self, initial_state=None):
        if initial_state is None:
            # Player 1 moves left, and player 2 moves right
            self.points = [
                [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0]
            ]
            self.bar = [0, 0] # Bar for player 1 and 2
            self.borne_off = [0, 0] # Borne off for player 1 and 2
            self.current_player = 0
        else:
            self.points = initial_state['points']
            self.bar = initial_state['bar']
            self.borne_off = initial_state['borne_off']
            self.current_player = initial_state['current_player']

    def roll_dice(self):
        """Simulate rolling two dice"""
        return random.randint(1, 6), random.randint(1, 6)

    def move_piece(self, player, src, dst):
        """Move a piece from source to destination point"""
        self.points[player][src] -= 1
        self.points[player][dst] += 1

        if (player == 0 and dst < 0) or (player == 1 and dst >= 24):
            print("bearing off piece")
            self.bear_off_piece(player, src)

    def hit_piece(self, player, pos):
        """Hit a piece and place it on the bar"""
        self.points[player][pos] -= 1
        self.bar[player] += 1

    def enter_piece(self, player, pos):
        """Enter a piece from the bar to the board"""
        self.bar[player] -= 1
        self.points[player][pos] += 1

    def bear_off_piece(self, player, pos):
        """Bear off a piece from the board"""
        self.points[player][pos] -= 1
        self.borne_off[player] += 1
    
    def is_legal_move(self, player, src, dst, dice):
        """Check if a move is legal"""
        # Check if dst is in board range
        if dst < 0 or dst >= 24: 
            print("checking dst")
            # Allow bearing off if all pieces are in the home board
            if player == 0 and all(point == 0 for point in self.points[player][0:6]):
                return True
            elif player == 1 and all(point == 0 for point in self.points[player][18:24]):
                return True
            return False
        
        # Check if src belongs to player
        if self.points[player][src] == 0: return False

        # Check if dst belongs to player or is empty
        if self.points[1 - player][dst] >= 2: return False

        # Check if dst is blocked
        if self.points[1 - player][dst] == 1: return False

        # Check if move is within range of rolled dice
        if abs(dst - src) not in dice: return False

        # Check if the player is moving in the correct direction
        if player == 0 and dst > src:
            return False  # Player 1 should move counterclockwise
        elif player == 1 and dst < src:
            return False  # Player 2 should move clockwise

        # Check if pieces on bar that needs to be entered
        if self.bar[player] > 0:
            # Check dst matches rolled dice
            if dst != dice[0] and dst != dice[1]:
                return False
        return True

    def get_legal_moves(self, player, dice):
        """Get all legal moves for a player given the dice roll"""
        legal_moves = []
        for src in range(24):
            for dst in range(24):
                if self.is_legal_move(player, src, dst, dice):
                    legal_moves.append((src, dst))

        return legal_moves
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.borne_off[0] == 15 or self.borne_off[1] == 15

    def reset_board(self):
        """Reset board to the initial state"""
        self.points = [[0]*24, [0]*24]
        self.bar = [0, 0]
        self.borne_off[0, 0]

    def calculate_final_score(self):
        """Calculate the final score of the game"""
        return self.borne_off[0], self.borne_off[1]
    
    def display_board_state(self):
        """Display the current state of the board"""
        print("Player 1 Points:", self.points[0])
        print("Player 2 Points:", self.points[1])
        print("Player 1 Bar:", self.bar[0])
        print("Player 2 Bar:", self.bar[1])
        print("Player 1 Borne Off:", self.borne_off[0])
        print("Player 2 Borne Off:", self.borne_off[1])

