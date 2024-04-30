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
        dice_list = [random.randint(1, 6), random.randint(1, 6)]
        if(dice_list[0] == dice_list[1]):
            dice_list.append(dice_list[0])
            dice_list.append(dice_list[0])
            
        return dice_list

    def move_piece(self, player, src, dst):
        if self.bar[player] == 0:
            if self.points[player][src] <= 0: return
            """Move a piece from source to destination point"""
            if (player == 0 and dst < 0):
                self.bear_off_piece(player, src)
            elif (player == 1 and dst >= 24):
                self.bear_off_piece(player, src)
            elif self.points[1-player][dst] == 1:
                self.points[player][src] -= 1
                self.points[player][dst] += 1
                self.hit_piece(1-player, dst)
            else:
                self.points[player][src] -= 1
                self.points[player][dst] += 1
        else:
            """Move piece from bar if possible"""
            self.bar[player] -= 1
            self.points[player][dst] += 1
            if self.points[1-player][dst] == 1:
                self.hit_piece(1-player, dst)

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
        if (player == 0 and dst == -1):
            if (sum(self.points[player][:6]) == 15 - self.borne_off[player]):
                return True
            else: return False
        elif (player == 0 and dst < -1):
            if(sum(self.points[player][:src+1]) == 15 - self.borne_off[player]):
                return True
            else: return False
        elif (player == 1 and dst == 24):
            if sum(self.points[player][18:]) == 15 - self.borne_off[player]:
                return True
            else: return False
        elif (player == 1 and dst > 24):
            if(sum(self.points[player][src:]) == 15 - self.borne_off[player]):
                return True
            else: return False
        
        # Check if src belongs to player
        if self.points[player][src] <= 0: return False

        # Check if dst is blocked
        if self.points[1 - player][dst] >= 2: return False

        # Check if move is within range of rolled dice
        if abs(dst - src) not in dice: return False

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
                if dst != dice[0] and dst != dice[1]:
                    return False
        return True

    def get_all_possible_moves(self, player, dice):
        """Generate all possible moves for a player and the dice roll"""
        moves = []
        for src, pieces in enumerate(self.points[player]):
            if pieces > 0:
                for d in dice:
                    new_dst = src - d if player == 0 else src + d 
                    moves.append((src, new_dst))
        return moves

    def get_legal_moves(self, player, dice):
        """Get all legal moves for a player given the dice roll"""
        all_moves = self.get_all_possible_moves(player, dice)
        legal_moves = []
        if self.bar[player] > 0:
            for d in dice:
                """Checks and makes sure that there are no more than 1 of the enemy pices on the position"""
                if player == 0 and self.points[1-player][24-d] < 2:
                    legal_moves.append((0, 24-d))
                elif player == 1 and self.points[1-player][d-1] < 2:
                    legal_moves.append((0, d-1))
        else:
            for move in all_moves:
                if self.is_legal_move(player, move[0], move[1], dice):
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

