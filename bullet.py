import pygame
from pygame.sprite import Sprite
import game_functions as gf

class Bullet(Sprite):
    def __init__(self,ai_settings, screen, ship, bullet_name, enemy=None):
        super(Bullet, self).__init__()
        self.screen = screen

        self.rect = pygame.Rect(-20,0, ai_settings.bullet_width, ai_settings.bullet_height)

        self.define_pos(ship, enemy, bullet_name)
        self.y = float(self.rect.y)

        self.speed_factor = ai_settings.bullet_speed_factor

        self.define_bullet(ai_settings, bullet_name)

    def define_pos(self, ship, enemy, bullet_name):
        if bullet_name == 'enemy':
            if enemy != None:
                self.rect.centerx = enemy.rect.centerx
                self.rect.bottom = enemy.rect.bottom
        elif bullet_name == 'player':
            self.rect.centerx = ship.rect.centerx
            self.rect.top = ship.rect.top

    def define_bullet(self, ai_settings, bullet_name):
        if bullet_name == 'enemy':
            self.bullet_image = ai_settings.bullet_image_enemy
        elif bullet_name == 'player':
            self.bullet_image = ai_settings.bullet_image_player

    def update(self, bullet_name):
        if bullet_name == 'enemy':
            self.y += self.speed_factor
            self.rect.y = self.y
        elif bullet_name == 'player':
            self.y -= self.speed_factor
            self.rect.y = self.y

    def draw_bullet(self, screen):
        screen.blit(self.bullet_image, self.rect)
