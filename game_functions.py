import sys
import pygame
from random import choice
from time import sleep
from timer import Timer
from bullet import Bullet
from alien import Alien
from blocker import Blocker
from explosion import Alien_explosion, Boss_explosion, Ship_explosion
from alien import Boss
from button import Button

def check_events(ai_settings, screen, stats, sb, main_menu, ship, aliens1, aliens2, aliens3, bullets, blockers, bosses, explosion_group, playagain_button, highest_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if stats.game_active :
                check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            if not stats.game_active and not stats.game_over:
                check_main_menu(ai_settings, screen, stats, sb, main_menu, ship, aliens1, aliens2, aliens3, bullets, blockers, bosses, explosion_group)
            else:
                check_keyup_events(event, ship)
                stats.play_again = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_click_button(ai_settings, screen, stats, sb, main_menu, playagain_button, highest_button, ship, aliens1, aliens2, aliens3, bullets, mouse_x, mouse_y, blockers, bosses, explosion_group)
        elif event.type == pygame.K_ESCAPE:
            sys.exit()

def check_main_menu(ai_settings, screen, stats, sb, main_menu, ship, aliens1, aliens2, aliens3, bullets, blockers, bosses, explosion_group):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()

    aliens1.empty()
    aliens2.empty()
    aliens3.empty()
    explosion_group.empty()
    bosses.empty()
    bullets.empty()

    blockers.empty()
    blockers.add(create_blockers(0))
    blockers.add(create_blockers(1))
    blockers.add(create_blockers(2))
    blockers.add(create_blockers(3))
    blockers.add(create_blockers(4))
    blockers.add(create_blockers(5))

    create_boss(bosses)
    create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3)
    ship.center_ship()

def create_boss(bosses):
    boss = Boss()
    bosses.add(boss)

def check_keydown_events(event, ai_settings, screen, ship, bullets_player):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
       fire_bullet(ai_settings,screen,ship, bullets_player)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_click_button(ai_settings, screen, stats, sb, main_menu, playagain_button,highest_button, ship, aliens1, aliens2, aliens3, bullets, mouse_x, mouse_y, blockers, bosses, explosion_group):
    if highest_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_over:
        ai_settings.show_high_score = True

    if playagain_button.rect.collidepoint(mouse_x,mouse_y) and stats.game_over:
        check_main_menu(ai_settings, screen, stats, sb, main_menu, ship, aliens1, aliens2, aliens3, bullets,
                            blockers, bosses, explosion_group)

def update_screen(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, main_menu, blockers, bosses, bullets_enemy, explosion_group, boss_explo, ship_explo, playagain_button, highest_button):
    screen.blit(ai_settings.backgroundImage, (0, 0))
    currentTime = pygame.time.get_ticks()
    if not stats.game_active:
        if stats.play_again:
            if not ai_settings.show_high_score:
                main_menu.draw_menu(stats)
                highest_button.draw_button()
            else:
                create_highest_UI(ai_settings, screen, playagain_button, stats)
        else:
            create_game_over(ai_settings, screen, playagain_button, stats)
    else:
        for bullet in bullets_player.sprites():
            bullet.draw_bullet(screen)
        for bullet in bullets_enemy.sprites():
            bullet.draw_bullet(screen)
        aliens1.draw(screen)
        aliens2.draw(screen)
        aliens3.draw(screen)
        explosion_group.draw(screen)
        boss_explo.update(screen)
        blockers.draw(screen)

        if not ai_settings.ship_crash:
            ship.blitme()
        else:
            if currentTime - ai_settings.ship_crash_time >= 500:
                ai_settings.ship_crash = False
                ship.blitme()
            ship_explo.draw(screen)

        make_enemies_shoot(ai_settings, screen, ship, bullets_enemy, aliens1, aliens2, aliens3, currentTime)
        bosses.update(currentTime, screen, ai_settings)


        sb.show_score()

    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, blockers, bosses, bullets_enemy, explosion_group, boss_explo):
    bullets_player.update('player')
    bullets_enemy.update('enemy')
    for bullet in bullets_player.copy():
        if bullet.rect.bottom <= 0:
            bullets_player.remove(bullet)
    for bullet in bullets_enemy.copy():
        if bullet.rect.top >= ai_settings.screen_height:
            bullets_enemy.remove(bullet)
    check_bullet_blockers_collisions(blockers, bullets_player, aliens1, aliens2, aliens3, bullets_enemy)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bosses, explosion_group, boss_explo)
    check_bullet_bullet_collision(bullets_player, bullets_enemy)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bosses, explosion_group, boss_explo):
    collisions1 = pygame.sprite.groupcollide(bullets_player, aliens1, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets_player, aliens2, True, True)
    collisions3 = pygame.sprite.groupcollide(bullets_player, aliens3, True, True)
    collisions4 = pygame.sprite.groupcollide(bullets_player, bosses, True, True)
    if collisions1:
        for aliens1 in collisions1.values():
            for x in aliens1:
                aliens1_explosion = Alien_explosion(screen, x, 'images/explosiongreen.png', 'images/explosiongreen2.png')
                explosion_group.add(aliens1_explosion)
            stats.score += ai_settings.alien1_points
            sb.prep_score()
        check_high_score(stats,sb)
    if collisions2:
        for aliens2 in collisions2.values():
            for x in aliens2:
                aliens2_explosion = Alien_explosion(screen, x, 'images/explosionblue.png',
                                                    'images/explosionblue2.png')
                explosion_group.add(aliens2_explosion)
            stats.score += ai_settings.alien2_points
            sb.prep_score()
        check_high_score(stats,sb)
    if collisions3:
        for aliens3 in collisions3.values():
            for x in aliens3:
                aliens3_explosion = Alien_explosion(screen, x, 'images/explosionpurple.png', 'images/explosionpurple2.png')
                explosion_group.add(aliens3_explosion)
            stats.score += ai_settings.alien3_points
            sb.prep_score()

        check_high_score(stats,sb)
    if collisions4:
        for bosses in collisions4.values():
            for x in bosses:
                aliens4_explosion = Boss_explosion(ai_settings, screen, x)
                boss_explo.add(aliens4_explosion)
            stats.score += ai_settings.boss_points
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens1) == 0 and len(aliens2) == 0 and len(aliens3) == 0:
        bullets_player.empty()
        ai_settings.increase_speed()

        stats.level += 1
        ai_settings.alien1_points += 5
        ai_settings.alien2_points += 5
        ai_settings.alien3_points += 5
        for i in range(4):
            ai_settings.boss_points_set[i] += 20
        sb.prep_level()
        create_boss(bosses)
        create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3)

    if collisions1 or collisions2 or collisions3:
        alien_destory_sound = pygame.mixer.Sound('sounds/alienkilled.wav')
        alien_destory_sound.set_volume(0.2)
        alien_destory_sound.play()
    if collisions4:
        boss_destory_sound = pygame.mixer.Sound('sounds/bosskilled.wav')
        boss_destory_sound.set_volume(0.2)
        boss_destory_sound.play()

def check_bullet_bullet_collision(bullets_player, bullets_enemy):
    collisions = pygame.sprite.groupcollide(bullets_player, bullets_enemy, True, True)

def check_bullet_blockers_collisions(blockers, bullets_player, aliens1, aliens2, aliens3, bullets_enemy):
    collisions1 = pygame.sprite.groupcollide(bullets_player, blockers, True, True)
    collisions2 = pygame.sprite.groupcollide(bullets_enemy, blockers, True, True)
    pygame.sprite.groupcollide(aliens1, blockers, False, True)
    pygame.sprite.groupcollide(aliens2, blockers, False, True)
    pygame.sprite.groupcollide(aliens3, blockers, False, True)

def fire_bullet(ai_settings, screen, ship, bullets_player):
    if len(bullets_player) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship, 'player')
        bullets_player.add(new_bullet)
        fire_sound = pygame.mixer.Sound('sounds/shoot.wav')
        fire_sound.set_volume(0.2)
        fire_sound.play()

def make_enemies_shoot(ai_settings, screen, ship, bullets_enemy, aliens1, aliens2, aliens3, time):
    if (pygame.time.get_ticks() - time) > 500 and aliens1 or aliens2 or aliens3:
        if len(bullets_enemy) < ai_settings.bullets_allowed:
            enemy = random_bottom(ai_settings, screen, aliens1, aliens2, aliens3, ship)
            bullets_enemy.add(Bullet(ai_settings, screen, ship, 'enemy', enemy))
            enemy_shoot_sound = pygame.mixer.Sound('sounds/shoot2.wav')
            enemy_shoot_sound.set_volume(0.2)
            enemy_shoot_sound.play()

        time = pygame.time.get_ticks()

def random_bottom(ai_settings, screen, aliens1, aliens2, aliens3, ship):
    alien1 = Alien(ai_settings, screen, 'images/enemy3_1.png', 'images/enemy3_2.png')
    number_aliens_x = get_number_aliens_x(ai_settings, alien1.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien1.rect.height)
    enemies = choice([aliens1, aliens2, aliens3])
    if enemies.sprites() == None:
        return None
    else:
        alien_left = []
        for x in enemies.sprites():
            alien_left.append(x)
        if len(alien_left) == 0:
            return None
        else:
            col_enemies = choice(alien_left)
            return col_enemies

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width - 200
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (6 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number, image_path1, image_path2):
    alien = Alien(ai_settings,screen, image_path1, image_path2)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_blockers(number):
    blockerGroup = pygame.sprite.Group()
    for row in range(4):
        for column in range(9):
            blocker = Blocker(10, (0, 255, 0), row, column)
            blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
            blocker.rect.y = 690 + (row * blocker.height)
            blockerGroup.add(blocker)
    return blockerGroup

def create_fleet(ai_settings, screen, ship, aliens1, aliens2, aliens3):
    alien1 = Alien(ai_settings, screen, 'images/enemy3_1.png', 'images/enemy3_2.png')
    number_aliens_x = get_number_aliens_x(ai_settings, alien1.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien1.rect.height)
    for row_number in range(4,number_rows ):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens1,alien_number, row_number, 'images/enemy3_1.png', 'images/enemy3_2.png')
    for row_number in range(2,4):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens2,alien_number, row_number, 'images/enemy2_1.png', 'images/enemy2_2.png')
    for alien_number in range(number_aliens_x):
        create_alien(ai_settings, screen, aliens3, alien_number, 1, 'images/enemy1_1.png', 'images/enemy1_2.png')

def update_aliens(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, explosion_group, ship_explo):
    check_fleet_edges(ai_settings,aliens1, aliens2, aliens3)
    aliens1.update()
    aliens2.update()
    aliens3.update()
    explosion_group.update(screen)

    if pygame.sprite.spritecollideany(ship, aliens1):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, ship_explo)
    elif pygame.sprite.spritecollideany(ship, aliens2):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, ship_explo)
    elif pygame.sprite.spritecollideany(ship, aliens3):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, ship_explo)
    elif pygame.sprite.spritecollideany(ship, bullets_enemy):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, ship_explo)

    ship_explo.update(screen, ship)
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player)

def check_fleet_edges(ai_settings, aliens1, aliens2, aliens3 ):

    for alien1 in aliens1.sprites():
        if alien1.check_edges() and not ai_settings.direction_change:
            change_fleet_direction(ai_settings, aliens1, aliens2, aliens3)
            break
    for alien2 in aliens2.sprites():
        if alien2.check_edges()and not ai_settings.direction_change:
            change_fleet_direction(ai_settings, aliens1, aliens2, aliens3)
            break
    for alien in aliens3.sprites():
        if alien.check_edges()and not ai_settings.direction_change:
            change_fleet_direction(ai_settings, aliens1, aliens2, aliens3)
            break
    ai_settings.direction_change = False

def change_fleet_direction(ai_settings, aliens1, aliens2, aliens3):
    for alien in aliens1.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in aliens2.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for alien in aliens3.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    ai_settings.direction_change_time += 1
    ai_settings.direction_change = True

def ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, bullets_enemy, ship_explo):
    ship_destory_sound = pygame.mixer.Sound( 'sounds/shipexplosion.wav')
    ship_destory_sound.set_volume(0.2)
    ship_destory_sound.play()
    ship_explosion = Ship_explosion(screen, ship, 'images/explosionship.png','images/explosionship2.png', 'images/explosionship3.png')
    ship_explo.add(ship_explosion)
    if stats.ships_left > 1:
        stats.ships_left -= 1
        sb.prep_ships()
        bullets_player.empty()
        bullets_enemy.empty()
        ai_settings.direction_change = False
        ai_settings.direction_change_time = 0
        ai_settings.ship_crash = True
        ai_settings.ship_crash_time = pygame.time.get_ticks()
        ship.center_ship()

    else:
        stats.game_active = False
        save_high_score(stats, sb)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player):
    screen_rect = screen.get_rect()
    for alien in aliens1.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, ship_explo)
            break
    for alien in aliens2.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, ship_explo)
            break
    for alien in aliens3.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens1, aliens2, aliens3, bullets_player, ship_explo)
            break

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def create_game_over(ai_settings, screen, playagain_button, stats):
    stats.game_over = True
    pygame.mouse.set_visible(True)
    gameoverImage = pygame.image.load('images/gameover.png')
    gameoverImage = pygame.transform.scale(gameoverImage, (ai_settings.screen_width, ai_settings.screen_height))
    screen.blit(gameoverImage, (0, 0))
    playagain_button.draw_button()

def create_highest_UI(ai_settings, screen, playagain_button, stats):
    gameoverImage = pygame.image.load('images/background.jpg')
    gameoverImage = pygame.transform.scale(gameoverImage, (ai_settings.screen_width, ai_settings.screen_height))
    screen.blit(gameoverImage, (0, 0))

    font_large = pygame.font.SysFont(None, 50)
    font_small = pygame.font.SysFont(None, 25)

    highestText = font_large.render('HIGH SCORE TOP 5', True, (237, 28, 36), gameoverImage)
    highestText_rect = highestText.get_rect()
    highestText_rect.center = (ai_settings.screen_width / 2, 200)

    no1Text = font_small.render(str(stats.high_score_list[0]), True, (237, 28, 36), gameoverImage)
    no1Text_rect = no1Text.get_rect()
    no1Text_rect.center = (ai_settings.screen_width / 2, 300)

    no2Text = font_small.render(str(stats.high_score_list[1]), True, (237, 28, 36), gameoverImage)
    no2Text_rect = no2Text.get_rect()
    no2Text_rect.center = (ai_settings.screen_width / 2, 350)

    no3Text = font_small.render(str(stats.high_score_list[2]), True, (237, 28, 36), gameoverImage)
    no3Text_rect = no3Text.get_rect()
    no3Text_rect.center = (ai_settings.screen_width / 2, 400)

    no4Text = font_small.render(str(stats.high_score_list[3]), True, (237, 28, 36), gameoverImage)
    no4Text_rect = no4Text.get_rect()
    no4Text_rect.center = (ai_settings.screen_width / 2, 450)

    no5Text = font_small.render(str(stats.high_score_list[4]), True, (237, 28, 36), gameoverImage)
    no5Text_rect = no5Text.get_rect()
    no5Text_rect.center = (ai_settings.screen_width / 2, 500)

    playText = font_small.render('Press any key to play', True, (255, 255, 255), gameoverImage)
    playText_rect = playText.get_rect()
    playText_rect.center = (ai_settings.screen_width / 2, 600)

    screen.blit(highestText, highestText_rect)
    screen.blit(no1Text, no1Text_rect)
    screen.blit(no2Text, no2Text_rect)
    screen.blit(no3Text, no3Text_rect)
    screen.blit(no4Text, no4Text_rect)
    screen.blit(no5Text, no5Text_rect)
    screen.blit(playText, playText_rect)

def save_high_score(stats, sb):
    file = open("highscore.txt", "a")
    file.write(str(stats.high_score) + ';')
    file.close()




