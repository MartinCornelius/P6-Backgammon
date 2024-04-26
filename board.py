# board.py

import random
import copy

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
            self.points = copy.deepcopy(initial_state['points'])
            self.bar = initial_state['bar']
            self.borne_off = initial_state['borne_off']
            self.current_player = initial_state['current_player']

    def roll_dice(self):
        """Simulate rolling two dice"""
        return random.randint(1, 6), random.randint(1, 6)

    def move_piece(self, player, src, dst):
        if self.points[player][src] <= 0: return
        """Move a piece from source to destination point"""
        if (player == 0 and dst < 0):
            if sum(self.points[player][:6]) == 15 - self.borne_off[player]:
                self.bear_off_piece(player, src)
        elif (player == 1 and dst >= 24):
            if sum(self.points[player][18:]) == 15 - self.borne_off[player]:
                self.bear_off_piece(player, src)
        else:
            self.points[player][src] -= 1
            self.points[player][dst] += 1

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
    
    def is_legal_move(self, player, src, dst, die):
        """Check if a move is legal"""
        if (player == 0 and dst < 0):
            if sum(self.points[player][:6]) == 15 - self.borne_off[player]:
                return True
            else: return False
        elif (player == 1 and dst >= 24):
            if sum(self.points[player][18:]) == 15 - self.borne_off[player]:
                return True
            else: return False
        
        # Check if src belongs to player
        if self.points[player][src] <= 0: return False

        # Check if dst belongs to player or is empty
        if self.points[1 - player][dst] >= 2: return False

        # Check if dst is blocked
        if self.points[1 - player][dst] == 1: return False

        # Check if move is within range of rolled dice
        if abs(dst - src) != die: return False

        # Check if bearing off
        if (player == 0 and dst < 0) or (player == 1 and dst >= 24):
            return True

        # Check if the player is moving in the correct direction
        if player == 0 and dst > src:
            return False  # Player 1 should move counterclockwise
        elif player == 1 and dst < src:
            return False  # Player 2 should move clockwise

        # Check if pieces on bar that needs to be entered
        if self.bar[player] > 0:
            if player == 1:
                if self.points[player][dst] == 0:
                    return True
            else:
                if dst != die:
                    return False
        return True

    def get_all_possible_moves(self, player, die):
        """Generate all possible moves for a player and the dice roll"""
        moves = []
        for src in range(24):
            new_dst = src - die if player == 0 else src + die 
            moves.append((src, new_dst))
            if player == 0 and new_dst < 0: 
                for i in range(1, abs(new_dst) + 1):
                    moves.append((src, new_dst - i))
            elif player == 1 and new_dst >= 24: 
                for i in range(1, 24 - new_dst + 1):
                    moves.append((src, new_dst + i))
        return moves

    def get_legal_moves(self, player, die):
        """Get all legal moves for a player given the dice roll"""
        all_moves = self.get_all_possible_moves(player, die)
        legal_moves = []
        for move in all_moves:
            if self.is_legal_move(player, move[0], move[1], die):
                legal_moves.append(move)
        return legal_moves

    def is_game_over(self):
        """Check if the game is over"""
        return self.borne_off[0] == 15 or self.borne_off[1] == 15

    def copy(self):
        """Creates a deep copy of the board"""
        return Board({
            'points': [player[:] for player in self.points],
            'bar': self.bar[:],
            'borne_off': self.borne_off[:],
            'current_player': self.current_player
        })
        
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

