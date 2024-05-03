import unittest
import random
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_bar_entering(self):
        self.board = Board({
            "points": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "bar": [1, 1],
            "borne_off": [0, 0],
            "current_player": 0
        })
        """Player 1 gets legal moves and moves"""
        legal_moves = self.board.get_legal_moves(self.board.current_player, (1, 1))
        if(len(legal_moves) > 0):
            self.board.move_piece(0, legal_moves[0][0], legal_moves[0][1])

        """Player 2 gets legal moves and moves"""
        legal_moves = self.board.get_legal_moves(1-self.board.current_player, (1, 1))
        if(len(legal_moves) > 0):
            self.board.move_piece(1, legal_moves[1][0], legal_moves[1][1])

        """Check if performed move was correct"""
        eval = self.board.points[0][0] == 1 and self.board.bar[0] == 0 and self.board.points[1][23] == 1 and self.board.bar[1] == 0
        self.assertTrue(eval)

    def test_initialization(self):
        self.assertEqual(self.board.points, [
            [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0]
        ])
        self.assertEqual(self.board.bar, [0, 0])
        self.assertEqual(self.board.borne_off, [0, 0])
        self.assertEqual(self.board.current_player, 0)

    def test_roll_dice_inrange(self):
        # Test roll_dice is within range
        dice_list = self.board.roll_dice()
        self.assertTrue(1 <= dice_list[0] <= 6)
        self.assertTrue(1 <= dice_list[1] <= 6)

    def test_roll_dice_list_length(self):
        expected_list = [6, 1]
        expected_list_len = len(expected_list)
        random.seed(42)
        dice_list = self.board.roll_dice()
        dice_list_len = len(dice_list)
        self.assertEqual(dice_list_len, expected_list_len)
    
    def test_roll_dice_insert_to_list(self):
        # Test roll_dice insert correctly into list.
        expected_list = [6, 1]
        random.seed(42)
        dice_list = self.board.roll_dice()
        self.assertListEqual(dice_list, expected_list)

    def test_roll_dice_doubling(self):
        # Test doubling in roll_dice
        expected_list = [4, 4, 4, 4]
        random.seed(0)
        dice_list = self.board.roll_dice()
        self.assertListEqual(dice_list, expected_list)

    def test_roll_dice_doubling_list_length(self):
        expected_list = [4, 4, 4, 4]
        expected_list_len = len(expected_list)
        random.seed(0)
        dice_list = self.board.roll_dice()
        dice_list_len = len(dice_list)
        self.assertEqual(dice_list_len, expected_list_len)

    def test_move_piece(self):
        # Test moving a piece from a point to another
        self.board.move_piece(0, 5, 4)
        self.assertEqual(self.board.points[0][4], 1)
        self.assertEqual(self.board.points[0][5], 4)

    def test_move_piece_from_bar(self):
        # Test moving a piece from the bar to a point
        pass

    def test_bear_off_piece(self):
        pass

    def test_hit_piece(self):
        self.board = Board({
            "points": [[1, 0],[0, 1]],
            "bar": [0, 0],
            "borne_off": [0, 0],
            "current_player": 0
        })
        self.board.move_piece(0, 0, 1)
        eval = self.board.points[0][1] == 1 and self.board.points[1][1] != 1
        self.assertTrue(eval)
        

    def test_is_gameover(self):
        self.board = Board({
            "points": [[0, 0, 0],[0, 0, 0]],
            "bar": [0, 0],
            "borne_off": [0, 15],
            "current_player": 0
        })
        self.assertTrue(self.board.is_game_over())
    
    def test_not_gameover(self):
        self.board = Board({
            "points": [[0, 0, 0],[0, 0, 0]],
            "bar": [0, 0],
            "borne_off": [2, 14],
            "current_player": 0
        })
        self.assertFalse(self.board.is_game_over())

    def test_overshoot_only_legal_move(self):
        # Arrange
        self.board = Board({
            "points": [[1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0],[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0]],
            "bar": [0, 0],
            "borne_off": [13, 0],
            "current_player": 0
        })
        dice = 5, 6

        # Act
        legal_moves = self.board.get_legal_moves(self.board.current_player, dice)
        print(f"legal_moves: {legal_moves}")
        only_move = [(2,-3),(2,-4)]
        print(f"only_move: {only_move}")

        # Assert
        self.assertEquals(legal_moves, only_move)

    def test_get_all_possible_moves_returns_actual_moves(self):
        # Arrange
        self.board = Board({
            "points": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "bar": [0, 0],
            "borne_off": [0, 14],
            "current_player": 1
        })
        
        # Act
        dice = 1, 2
        all_moves = self.board.get_all_possible_moves(self.board.current_player, dice)
        expected_moves = [(0, 1), (0, 2)]

        # Assert
        self.assertEquals(all_moves, expected_moves)
