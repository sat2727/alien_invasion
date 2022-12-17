import sys
from time import sleep
import json

import pygame

from bullet import Bullet
from alien import Alien


def check_events(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    """Respond to key presses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('high_score.json', 'w') as file:
                json.dump(stats.high_score, file)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, sb, screen, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, sb, screen, ship, aliens, bullets,
                play_button, mouse_x, mouse_y)


def check_play_button(ai_settings, stats, sb, screen, ship, aliens, bullets, 
        play_button, mouse_x, mouse_y):
    """Starts a new game when a player clicks the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, stats, sb, screen, ship, aliens, bullets)


def start_game(ai_settings, stats, sb, screen, ship, aliens, bullets):
    # hide mouse cursor
    pygame.mouse.set_visible(False)

    ai_settings.initialize_dynamic_settings()

    stats.reset_stats()
    stats.game_active = True
    
    sb.prep_score()
    sb.prep_level()
    sb.prep_ships()

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_keydown_events(event, ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        with open('high_score.json', 'w') as file:
            json.dump(stats.high_score, file)
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        start_game(ai_settings, stats, sb, screen, ship, aliens, bullets)
    elif event.key == pygame.K_r:
        stats.high_score = 0
        sb.prep_high_score()
        

def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Update bullet positions and remove offscreen bullets"""
    # Update bullet positions
    bullets.update()

    # Get rid of the bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, stats, sb, screen, ship, bullets, aliens)


def check_bullet_alien_collisions(ai_settings, stats, sb, screen, ship, bullets, aliens):
    """
    Checks if any bullet hit an alien. If, so removes both.
    If an alien fleet is destroyed, it creates a new fleet.
    """
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if the maximum allowed isn't exceeded"""
    if len(bullets) < ai_settings.bullets_allowed:
        # create a new bullet and add it to the bullet group
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Determine the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create a row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    return int(available_space_x / (alien_width * 2))


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    return int(available_space_y / (2 * alien_height))


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien_height = alien.rect.height
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    check if an alien is at an edge,
    and then update the position of all aliens in fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any alien hit the screen bottom"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat it like a ship hit
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to the ship being hit by an alien"""
    
    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        bullets.empty()
        aliens.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, stats, sb, screen, ship, aliens, bullets, play_button):
    """Update images on screen and flips to the new screen"""
    # Redraw the screen during each pass of the loop 
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind the ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # display scoreboard
    sb.show_score()
    
    # draw play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
   

    # Make the most recently drawn screen visible
    pygame.display.flip()
