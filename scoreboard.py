import pygame
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeepung attributes"""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)

        # prep initial scoreboard images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score :,}"
        self.score_image = self.font.render(score_str, True, self.text_color,
            self.ai_settings.bg_color)
        
        # display the score at the top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 10
        self.score_rect.right = self.screen_rect.right - 10

    def prep_high_score(self):
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = f"{rounded_high_score :,}"
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.ai_settings.bg_color)

        # center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = self.score_rect.top
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True,
            self.text_color, self.ai_settings.bg_color)
        
        # position level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.score_rect.right

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.image = pygame.transform.scale(ship.image,
                (ship.rect.width * .75, ship.rect.height * .75))
            ship.rect.y = 10
            ship.rect.x = 10 + ship_number * ship.rect.width
            self.ships.add(ship)

    def show_score(self):
        """Draw scoreboard to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.ships.draw(self.screen)