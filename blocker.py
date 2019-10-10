import pygame
from pygame.sprite import Sprite

class Blocker(Sprite):
    def __init__(self, size, color, row, column):
        super(Blocker, self).__init__()
        self.height = size
        self.width = size
        self.color = color
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.column = column
