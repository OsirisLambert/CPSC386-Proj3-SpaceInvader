import sys
import pygame
import game_functions as gf

from settings import  Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Main_menu, Button
from ship import Ship
from alien import Alien
from blocker import Blocker
from pygame.sprite import Group

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    ship = Ship(ai_settings,screen)
    pygame.display.set_caption("Alien Invasion")
    stats = GameStats(ai_settings)
    main_menu = Main_menu(ai_settings, screen, stats)
    playagain_button = Button(ai_settings, screen, 'PLAY AGAIN', ai_settings.screen_width / 2, 100)
    highest_button = Button(ai_settings, screen, 'HIGH SCORE', ai_settings.screen_width / 2, 600)
    sb = Scoreboard(ai_settings, screen, stats)
    bullets_player = Group()
    bullets_enemy = Group()
    aliens1 = Group()
    aliens2 = Group()
    aliens3 = Group()
    explosion_group = Group()
    boss_explo = Group()
    ship_explo = Group()
    bosses = Group()
    blockers = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3)
    past = 0

    while True:
        now = pygame.time.get_ticks()

        gf.check_events(ai_settings, screen, stats, sb, main_menu, ship, aliens1, aliens2, aliens3, bullets_player, blockers, bosses, explosion_group, playagain_button, highest_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, blockers, bosses, bullets_enemy, explosion_group, boss_explo)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, explosion_group, ship_explo)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, main_menu, blockers, bosses, bullets_enemy, explosion_group, boss_explo, ship_explo, playagain_button, highest_button)

        if now - past >= 500:
            past = now
            explosion_group.empty()
            boss_explo.empty()
            if not ai_settings.ship_crash:
                ship_explo.empty()

run_game()