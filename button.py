import pygame.font

class Main_menu():
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)

        self.WHITE = (255, 255, 255)
        self.GREEN = (78, 255, 87)
        self.YELLOW = (241, 255, 0)
        self.BLUE = (80, 255, 239)
        self.PURPLE = (203, 0, 255)
        self.RED = (237, 28, 36)

        self.font_large = pygame.font.SysFont(None, 50)
        self.font_small = pygame.font.SysFont(None, 25)

        self.prep_msg()
        self.prep_image()

    def prep_image(self):
        self.enemy1Image = pygame.image.load('images/enemy3_1.png')
        self.enemy1Image = pygame.transform.scale(self.enemy1Image, (40, 40))

        self.enemy2Image = pygame.image.load('images/enemy2_1.png')
        self.enemy2Image = pygame.transform.scale(self.enemy2Image, (40, 40))

        self.enemy3Image = pygame.image.load('images/enemy1_1.png')
        self.enemy3Image = pygame.transform.scale(self.enemy3Image, (40, 40))

        self.enemy4Image = pygame.image.load('images/mystery.png')
        self.enemy4Image = pygame.transform.scale(self.enemy4Image, (80, 40))

    def prep_msg(self):
        self.titleText = self.font_large.render('Space Invaders', True, self.WHITE, self.screen)
        self.titleText_rect = self.titleText.get_rect()
        self.titleText_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 200)

        self.titleText2 = self.font_small.render('Press any key to continue', True, self.WHITE, self.screen)
        self.titleText2_rect = self.titleText2.get_rect()
        self.titleText2_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 150)

        self.enemy1Text = self.font_small.render('   =   10 pts', True, self.GREEN, self.screen)
        self.enemy1Text_rect = self.enemy1Text.get_rect()
        self.enemy1Text_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 50)

        self.enemy2Text = self.font_small.render('   =  20 pts', True, self.BLUE, self.screen)
        self.enemy2Text_rect = self.enemy2Text.get_rect()
        self.enemy2Text_rect.center = (self.screen_rect.centerx, self.screen_rect.centery)

        self.enemy3Text = self.font_small.render('   =  30 pts', True, self.PURPLE, self.screen)
        self.enemy3Text_rect = self.enemy3Text.get_rect()
        self.enemy3Text_rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 50)


        self.enemy4Text = self.font_small.render('   =  ?????', True, self.RED, self.screen)
        self.enemy4Text_rect = self.enemy4Text.get_rect()
        self.enemy4Text_rect.center = (self.screen_rect.centerx, self.screen_rect.centery + 100)


    def draw_menu(self, stats):
        self.screen.blit(self.titleText, self.titleText_rect)
        self.screen.blit(self.titleText2, self.titleText2_rect)
        self.screen.blit(self.enemy1Text, self.enemy1Text_rect)
        self.screen.blit(self.enemy2Text, self.enemy2Text_rect)
        self.screen.blit(self.enemy3Text, self.enemy3Text_rect)
        self.screen.blit(self.enemy4Text, self.enemy4Text_rect)

        self.screen.blit(self.enemy1Image, (self.screen_rect.centerx - 100, self.screen_rect.centery - 75))
        self.screen.blit(self.enemy2Image, (self.screen_rect.centerx - 100, self.screen_rect.centery - 25))
        self.screen.blit(self.enemy3Image, (self.screen_rect.centerx - 100, self.screen_rect.centery + 25))
        self.screen.blit(self.enemy4Image, (self.screen_rect.centerx - 125, self.screen_rect.centery + 75))

class Button():
    def __init__(self, ai_settings, screen, msg, x, y):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 600, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x
        self.rect.y = y

        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)