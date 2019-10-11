import pygame
import sys
from pygame.sprite import Sprite
from timer import Timer
from random import choice

class Alien_explosion(Sprite):
    def __init__(self, screen, alien, image_path1, image_path2):
        super(Alien_explosion, self).__init__()
        self.images = []
        self.create_animate_image(image_path1, image_path2)
        self.image_timer = Timer(self.images, 100, 0, 1, True)
        self.image = self.image_timer.imagerect()
        self.rect = self.image.get_rect(topleft=(alien.rect.x, alien.rect.y))

    def create_animate_image(self,image_path1, image_path2):
        self.temp1 = pygame.image.load(image_path1)
        self.temp1 = pygame.transform.scale(self.temp1, (40, 40))
        self.temp2 = pygame.image.load(image_path2)
        self.temp2 = pygame.transform.scale(self.temp2, (40, 40))
        self.images.append(self.temp1)
        self.images.append(self.temp2)


    def update(self, screen):
        self.image = self.image_timer.imagerect()
        screen.blit(self.image, self.rect)


class Boss_explosion(Sprite):
    def __init__(self, ai_settings, screen, boss):
        super(Boss_explosion, self).__init__()
        self.font = pygame.font.SysFont(None, 30)
        self.text = self.font.render(str(ai_settings.boss_points), True, (255, 255, 255), screen)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (boss.rect.x + 20, boss.rect.y + 6)

    def update(self, screen):
        screen.blit(self.text, self.text_rect)

class Ship_explosion(Sprite):
    def __init__(self, screen, ship, image_path1, image_path2, image_path3, image_path4,
                 image_path5, image_path6, image_path7, image_path8):
        super(Ship_explosion, self).__init__()
        self.images = []
        self.create_animate_image(ship, image_path1, image_path2, image_path3, image_path4, image_path5, image_path6, image_path7, image_path8)
        self.image_timer = Timer(self.images, 30, 0, 7, True)
        self.image = self.image_timer.imagerect()
        self.rect = self.image.get_rect(topleft=(ship.rect.x - 15, ship.rect.y - 20))

    def create_animate_image(self, ship, image_path1, image_path2, image_path3, image_path4, image_path5, image_path6, image_path7, image_path8):
        self.temp1 = pygame.image.load(image_path1)
        self.temp1 = pygame.transform.scale(self.temp1, (80,80))
        self.temp2 = pygame.image.load(image_path2)
        self.temp2 = pygame.transform.scale(self.temp2, (80,80))
        self.temp3 = pygame.image.load(image_path3)
        self.temp3 = pygame.transform.scale(self.temp3, (80,80))
        self.temp4 = pygame.image.load(image_path4)
        self.temp4 = pygame.transform.scale(self.temp4, (80,80))
        self.temp5 = pygame.image.load(image_path5)
        self.temp5 = pygame.transform.scale(self.temp5, (80,80))
        self.temp6 = pygame.image.load(image_path6)
        self.temp6 = pygame.transform.scale(self.temp6, (80,80))
        self.temp7 = pygame.image.load(image_path7)
        self.temp7 = pygame.transform.scale(self.temp7, (80,80))
        self.temp8 = pygame.image.load(image_path8)
        self.temp8 = pygame.transform.scale(self.temp8, (80,80))

        self.images.append(self.temp8)
        self.images.append(self.temp7)
        self.images.append(self.temp6)
        self.images.append(self.temp5)
        self.images.append(self.temp4)
        self.images.append(self.temp3)
        self.images.append(self.temp2)
        self.images.append(self.temp1)








    def update(self, screen, ship):
        self.image = self.image_timer.imagerect()
        screen.blit(self.image, self.rect)

