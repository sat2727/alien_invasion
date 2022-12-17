import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from button import Button
import game_functions as gf



def main():
    run_game()


def run_game():
    # Initialize pygame, settings, stats, and screen object
    pygame.init()
    ai_settings = Settings()
    stats = GameStats(ai_settings)
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    sb = Scoreboard(ai_settings, screen, stats)
    pygame.display.set_caption("Alien Invasion")

    # make play button
    play_button = Button(ai_settings, screen, "Play")

    # Make a ship, a group of bullets, and a group of aliens 
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # create the fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop of the game.
    while True:
        gf.check_events(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button)

if __name__ == '__main__':
    main()