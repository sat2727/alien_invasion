import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""
    
    def __init__(self, ai_settings, screen):
        """intialize alien image and starting position"""
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        
        # load alien image and create its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # set each new alien position at the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the decimal position of the alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien hit a screen edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Draw the alien at set position"""
        self.screen.blit(self.image, self.rect)

