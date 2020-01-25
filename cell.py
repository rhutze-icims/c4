from config import *
import pygame


class Cell(pygame.sprite.Sprite):
    red = False  # What we hear from them
    black = False  # What we hear from them
    image = None  # Which image to draw

    def __init__(self, row, col, images):
        super().__init__()

        self.row = row
        self.col = col
        self.images = images
        self.rect = pygame.Rect((0, 0), (CELL_SIZE, CELL_SIZE))
        self.update()

    def update(self):
        if self.red:
            self.image = self.images['red']
        elif self.black:
            self.image = self.images['black']
        else:
            self.image = pygame.Surface([CELL_SIZE, CELL_SIZE])
            self.image.fill((0, 0, 0))

    def is_clickable_here(self, x, y):
        return self.rect.collidepoint(x, y) and not self.already_played()

    def record_move(self, color_of_move):
        if self.already_played():
            print('Cell [%d, %d] was already played.' % (self.row, self.col))
            return NOT_HANDLED

        if color_of_move == 'red':
            self.red = True
        else:
            self.black = True
        return HANDLED

    def already_played(self):
        return self.red or self.black

    def clear(self):
        self.red = False
        self.black = False

