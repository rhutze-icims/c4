from cell import Cell
from config import *
import pygame
import pygame.freetype


class Board:

    def __init__(self, pygame_font, grid_rows, grid_cols, x, y, images):
        self.font = pygame_font(None, 28)
        self.sprites = pygame.sprite.Group()

        self.board_x = x
        self.board_y = y
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.grid = [[Cell(row, col, images) \
            for col in range(grid_cols)] for row in range(grid_rows)]

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                cell = self.grid[row][col]
                self.sprites.add(cell)
                cell.rect.x = self.board_x + 30 + (col * (CELL_SIZE + 2))
                cell.rect.y = self.board_y + 30 + (row * (CELL_SIZE + 2))

    def make_move_click(self, x, y):
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if self.grid[row][col].is_clickable_here(x, y):
                    self.handle_column_clicked(col)
        self.sprites.update()

    def handle_column_clicked(self, clicked_column):
        # Start from the bottom of the column. Announce the next cell that can be filled, if any.
        for row in reversed(range(self.grid_rows)):
            if not self.grid[row][clicked_column].already_played():
                print('Moving into [%s][%s] ...' % (row, clicked_column))
                event = pygame.event.Event(pygame.USEREVENT, dict(action=ACTION_MAKE_MOVE, row=row, col=clicked_column))
                pygame.event.post(event)
                break
            else:
                print('Skipping [%s][%s] because it was already played.' % (row, clicked_column))

    def record_move(self, color_of_move, row, col):
        if self.grid[row][col].record_move(color_of_move):
            self.sprites.update()
            return HANDLED
        return NOT_HANDLED

    def draw(self, surface):
        self.sprites.draw(surface)

    def is_win(self):
        # Vertical win
        for col in range(self.grid_cols):
            winner = self.is_winning_col(col)
            if not winner is None:
                return winner

        # Horizontal win
        for row in range(self.grid_rows):
            winner = self.is_winning_row(row)
            if not winner is None:
                return winner

        # From left diagonal starting from each row and col
        for row_offset in range(self.grid_rows):
            for col_offset in range(self.grid_cols):
                winner = self.is_winner_from_diagonal(row_offset, col_offset, 'left')
                if not winner is None:
                    return winner

        # From right diagonal starting from each row and col
        for row_offset in range(self.grid_rows):
            for col_offset in range(self.grid_cols):
                winner = self.is_winner_from_diagonal(row_offset, col_offset, 'right')
                if not winner is None:
                    return winner

        return None

    def is_winning_row(self, row):
        red_tally = 0
        black_tally = 0
        for col in range(self.grid_cols):
            if self.grid[row][col].red:
                red_tally = red_tally + 1
                black_tally = 0
            elif self.grid[row][col].black:
                red_tally = 0
                black_tally = black_tally + 1
            else:
                red_tally = 0
                black_tally = 0

            if red_tally >= 4:
                return 'red'
            elif black_tally >= 4:
                return 'black'

        return None

    def is_winning_col(self, col):
        red_tally = 0
        black_tally = 0
        for row in range(self.grid_rows):
            if self.grid[row][col].red:
                red_tally = red_tally + 1
                black_tally = 0
            elif self.grid[row][col].black:
                red_tally = 0
                black_tally = black_tally + 1
            else:
                red_tally = 0
                black_tally = 0

            if red_tally >= 4:
                return 'red'
            elif black_tally >= 4:
                return 'black'

        return None

    def is_winner_from_diagonal(self, starting_row, starting_col, from_direction):
        red_tally = 0
        black_tally = 0
        row = starting_row
        col = starting_col

        while 0 <= row < self.grid_rows and 0 <= col < self.grid_cols:
            if self.grid[row][col].red:
                red_tally = red_tally + 1
                black_tally = 0
            elif self.grid[row][col].black:
                red_tally = 0
                black_tally = black_tally + 1
            else:
                red_tally = 0
                black_tally = 0

            if red_tally >= 4:
                return 'red'
            elif black_tally >= 4:
                return 'black'

            if from_direction == 'left':
                row = row + 1
                col = col + 1
            else:
                row = row + 1
                col = col - 1

        return None

    def clear_all_cells(self):
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                self.grid[row][col].clear()

    def state_of_all_cells(self, row_separator='-', col_separator=''):
        output = ""
        for row in range(self.grid_rows):
            if len(output) > 0:
                output += row_separator
            for col in range(self.grid_cols):
                if self.grid[row][col].red:
                    output += col_separator + "R" + col_separator
                elif self.grid[row][col].black:
                    output += col_separator + "B" + col_separator
                else:
                    output += col_separator + "." + col_separator
        return output

    def __str__(self):
        return self.state_of_all_cells('\n', ' ')

