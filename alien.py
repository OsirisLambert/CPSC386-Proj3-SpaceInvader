import pygame
import sys
from pygame.sprite import Sprite
from timer import Timer
from random import choice

class Alien(Sprite):
    def __init__(self, ai_settings, screen, image_path1, image_path2):
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.images = []
        self.create_animate_image(image_path1, image_path2)
        self.image_timer = Timer(self.images, 100, 0, 1, False)
        self.image = self.image_timer.imagerect()
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def create_animate_image(self,image_path1, image_path2):
        self.temp1 = pygame.image.load(image_path1)
        self.temp1 = pygame.transform.scale(self.temp1, (40, 40))
        self.temp2 = pygame.image.load(image_path2)
        self.temp2 = pygame.transform.scale(self.temp2, (40, 40))
        self.images.append(self.temp1)
        self.images.append(self.temp2)

    def update(self):
        self.image = self.image_timer.imagerect()
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blitme(self):
        self.screen.blit(self.image, self.rect)


class Boss(Sprite):
    def __init__(self):
        super(Boss, self).__init__()
        self.image = pygame.image.load('images/mystery.png')
        self.image = pygame.transform.scale(self.image, (80, 40))
        self.rect = self.image.get_rect(topleft=(-80, 80))
        self.row = 5
        self.moveTime = 1000
        self.direction = 1
        self.timer = pygame.time.get_ticks()
        self.mysteryEntered = pygame.mixer.Sound('sounds/mysteryentered.wav')
        self.mysteryEntered.set_volume(0.3)
        self.playSound = True

    def update(self, currentTime, screen, ai_settings):
        resetTimer = False
        passed = currentTime - self.timer
        if passed > self.moveTime:
            if (self.rect.x < 0 or self.rect.x > 800) and self.playSound:
                self.mysteryEntered.play()
                self.playSound = False
            if self.rect.x < ai_settings.screen_width + 100 and self.direction == 1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x += 2
                screen.blit(self.image, self.rect)
            if self.rect.x > -100 and self.direction == -1:
                self.mysteryEntered.fadeout(4000)
                self.rect.x -= 2
                screen.blit(self.image, self.rect)

        if self.rect.x > ai_settings.screen_width + 90:
            self.playSound = True
            self.direction = -1
            resetTimer = True
        if self.rect.x < -90:
            self.playSound = True
            self.direction = 1
            resetTimer = True
        if passed > self.moveTime and resetTimer:
            self.timer = currentTime
