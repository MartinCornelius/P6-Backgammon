import unittest
import random
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initialization(self):
        self.assertEqual(self.board.points, [
            [0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 5, 0, 0, 0, 0, 0]
        ])
        self.assertEqual(self.board.bar, [0, 0])
        self.assertEqual(self.board.borne_off, [0, 0])
        self.assertEqual(self.board.current_player, 0)

    def test_roll_dice(self):
        # Test roll_dice is within range
        dice_list = self.board.roll_dice()
        self.assertTrue(1 <= dice_list[0] <= 6)
        self.assertTrue(1 <= dice_list[1] <= 6)
        # Test roll_dice insert correctly into list.
        random.seed(42)
        dice_list = self.board.roll_dice()
        self.assertEqual(dice_list[0], 6)
        self.assertEqual(dice_list[1], 1)
        # Test doubling in roll_dice
        random.seed(0)
        dice_list = self.board.roll_dice()
        self.assertEqual(dice_list[0], 4)
        self.assertEqual(dice_list[1], 4)
        self.assertEqual(dice_list[2], 4)
        self.assertEqual(dice_list[3], 4)

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
        pass

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