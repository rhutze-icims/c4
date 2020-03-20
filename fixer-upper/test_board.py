from board import Board
import unittest
from unittest.mock import Mock


class TestBoard(unittest.TestCase):

    def setUp(self):
        mock_font = Mock()
        self.board = Board(mock_font, 6, 7, 0, 0, None)

    def test_is_red_vertical_win(self):
        self.board.grid[2][0].red = True
        self.board.grid[3][0].red = True
        self.board.grid[4][0].red = True
        self.board.grid[5][0].red = True
        self.assertEqual('red', self.board.is_win())

    def test_is_black_vertical_win(self):
        self.board.grid[2][1].black = True
        self.board.grid[3][1].black = True
        self.board.grid[4][1].black = True
        self.board.grid[5][1].black = True
        self.assertEqual('black', self.board.is_win())

    def test_other_color_interruption_is_not_win(self):
        self.board.grid[2][1].black = True
        self.board.grid[3][1].red = True
        self.board.grid[4][1].black = True
        self.board.grid[5][1].black = True
        self.assertIsNone(self.board.is_win())

    def test_empty_interruption_is_not_win(self):
        self.board.grid[2][1].black = True
        self.board.grid[3][1].black = False
        self.board.grid[4][1].black = True
        self.board.grid[5][1].black = True
        self.assertIsNone(self.board.is_win())

    def test_is_horizontal_win(self):
        self.board.grid[2][1].black = True
        self.board.grid[2][2].black = True
        self.board.grid[2][3].black = True
        self.board.grid[2][4].black = True
        self.assertEqual('black', self.board.is_win())

    def test_skipped_row_is_not_win(self):
        self.board.grid[1][0].red = True
        self.board.grid[2][0].red = True

        self.board.grid[3][0].black = True

        self.board.grid[4][0].red = True
        self.board.grid[5][0].red = True
        self.assertIsNone(self.board.is_win())

    def test_from_left_diagonal(self):
        self.board.grid[2][0].red = True
        self.board.grid[3][1].red = True
        self.board.grid[4][2].red = True
        self.board.grid[5][3].red = True
        print('From Left Diagonal: ')
        print(self.board)
        self.assertEqual('red', self.board.is_win())

    def test_from_centered_right_diagonal(self):
        self.board.grid[5][3].black = True
        self.board.grid[4][4].black = True
        self.board.grid[3][5].black = True
        self.board.grid[2][6].black = True
        print('From Center Right Diagonal: ')
        print(self.board)
        self.assertEqual('black', self.board.is_win())

    def test_from_top_right_diagonal(self):
        self.board.grid[0][5].black = True
        self.board.grid[1][4].black = True
        self.board.grid[2][3].black = True
        self.board.grid[3][2].black = True
        print('From Top Right Diagonal: ')
        print(self.board)
        self.assertEqual('black', self.board.is_win())

if __name__ == '__main__':
    unittest.main()
