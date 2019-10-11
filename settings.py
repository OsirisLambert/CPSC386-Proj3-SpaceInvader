import pygame
from random import choice

class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.backgroundImage = pygame.image.load('images/background.jpg')
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (self.screen_width, self.screen_height))

        self.music_index = 0
        self.music = [pygame.mixer.Sound('sounds/' + '{}.wav'.format(i)) for i
                           in range(4)]
        for sound in self.music:
            sound.set_volume(0.5)
        self.time_change = 0

        self.ship_speed_factor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1

        self.show_high_score = False
        self.ship_limit = 3
        self.ship_crash = False
        self.ship_crash_time = 0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_image_player = pygame.image.load('images/laser.png')
        self.bullet_image_enemy = pygame.image.load('images/enemylaser.png')
        self.bullets_allowed = 3

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1

        self.alien1_points = 10
        self.alien2_points = 20
        self.alien3_points = 30
        self.boss_points_set = [50, 100, 150, 300]
        self.boss_points = choice(self.boss_points_set)

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        self.ship_speed_facor = 2
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.direction_change_time = 0
        self.direction_change = False


    def increase_speed(self):
        self.ship_speed_facor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale


