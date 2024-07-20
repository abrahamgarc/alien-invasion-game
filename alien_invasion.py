import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Background
from leaderboard import Leaderboard

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to score game statistics, scoreboard and background.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.bg = Background(self)


        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the Play button.
        self.play_button = Button(self, "Play")

        # Make difficulty level and leaderboard buttons.
        self._make_difficulty_buttons()
        self._make_leaderboard_button()
        self._make_back_button()

        # Start Alien Invasion in an inactive state and the active screen.
        self.game_active = False
        self.menu_state = 'main'

        self.username = 'Enter Username:'
        self.username_input_active = False


    def _check_events(self):
        """Respond to keypresses and mouse events."""

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.menu_state == 'main':
                        self._check_play_button(mouse_pos)
                        self._check_difficulty_buttons(mouse_pos)
                        self._check_leaderboard_button(mouse_pos)
                    elif self.menu_state == 'leaderboard':
                        self._check_back_button(mouse_pos)


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif (event.key == pygame.K_p) and (not self.game_active):
            # Don't start a new game during an active game, that's probably an accidental keypress.
            self._start_game()   
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        # When user input is requested
        elif self.username_input_active:
                if self.username == "Enter Username:":
                    self.username = ""  # Clear the placeholder text on first key press
                    self.prompt_username_overlay()
                if event.key == pygame.K_RETURN:
                    self.username_input_active = False
                    self.stats.upload_packet(self.username)
                    # Save the username here or process it further
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode
        

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _start_game(self):
        """Start a new game."""

        if not self.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
             # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            self.game_active = True

            # Get rid of any remaning bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _make_difficulty_buttons(self):
        """Make buttons that allow player to select difficulty level."""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.hard_button = Button(self, "Hard")

        # Position buttons so they don't all overlap.
        self.easy_button.rect.top = (self.play_button.rect.top + 1.5 * self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (self.easy_button.rect.top + 1.5 * self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.hard_button.rect.top = (self.medium_button.rect.top + 1.5 * self.medium_button.rect.height)
        self.hard_button._update_msg_position()

    def _make_back_button(self):
        """Make button that allows player to go back to main menu from game leaderboard."""
        self.back_button = Button(self, "Back")
        self.back_button.change_settings()
        self.back_button.rect.topleft = (70, 130)
        self.back_button._update_msg_position()

    def _make_leaderboard_button(self):
        """make button that allows player to view game leaderboard."""
        self.leaderboard_button = Button(self, "Leaderboard")
        self.leaderboard_button.rect.top = self.play_button.rect.top - 1.5 * self.play_button.rect.height
        self.leaderboard_button._update_msg_position()

    def _check_leaderboard_button(self, mouse_pos):
        """Check if button has been pressed."""
        leaderboard_button_clicked = self.leaderboard_button.rect.collidepoint(mouse_pos)
        if leaderboard_button_clicked:
            self.leaderboard_button.set_highlighted_color()
            self.play_button.set_base_color()
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.hard_button.set_base_color()
            self.menu_state = 'leaderboard'

    def _check_back_button(self, mouse_pos):
        """Check if back button has been pressed."""
        back_button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if back_button_clicked:
            self.menu_state = 'main'

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play."""
        if self.play_button.rect.collidepoint(mouse_pos):
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.game_active:
                self._start_game()
            
    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(mouse_pos)
        hard_button_clicked = self.hard_button.rect.collidepoint(mouse_pos)
        if easy_button_clicked:
            self.settings.set_difficulty('easy')
            self.leaderboard_button.set_base_color()
            self.easy_button.set_highlighted_color()
            self.medium_button.set_base_color()
            self.hard_button.set_base_color()
        elif medium_button_clicked:
            self.settings.set_difficulty("medium")
            self.leaderboard_button.set_base_color()
            self.easy_button.set_base_color()
            self.medium_button.set_highlighted_color()
            self.hard_button.set_base_color()
        elif hard_button_clicked:
            self.settings.set_difficulty('hard')
            self.leaderboard_button.set_base_color()
            self.easy_button.set_base_color()
            self.medium_button.set_base_color()
            self.hard_button.set_highlighted_color()
        

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bulllets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destory existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()


        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding alien until there's no room left
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            
            # Get rif of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            self.username_input_active = True
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def leaderboard_screen(self):
        # Fill the screen with black when showing the leaderboard
        self.screen.fill((0, 0, 0))
        self.leaderboard = Leaderboard(self)
        self.leaderboard.draw_text()
        self.back_button.draw_button()



    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""

        if self.menu_state == 'leaderboard':
            self.leaderboard_screen()

        else:
            self.screen.fill(self.settings.bg_color)

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()
            self.aliens.draw(self.screen)

            # Draw the score information.
            self.sb.show_score()

        # Draw the button's if the game is inactive.
        if not self.game_active:
            if self.menu_state == 'main':
                self.bg.loading_screen()
                self.play_button.draw_button()
                self.leaderboard_button.draw_button()
                self.easy_button.draw_button()
                self.medium_button.draw_button()
                self.hard_button.draw_button()
                if self.username_input_active:
                    # DO THE USER INPUT
                    self.prompt_username_overlay()

    
        pygame.display.flip()

    def prompt_username_overlay(self):
        """Prompt the player to enter a username, displayed over the main menu."""

        font = pygame.font.Font('joystix.otf', 25)
        text_surface = font.render(self.username,True, (255,255,255))
        input_rect = pygame.Rect(0, 0, 255, 50)
        input_rect.center = (600, 159)

        text_rect = text_surface.get_rect(center=input_rect.center)
        text_rect.center = input_rect.center
        input_rect.w = max(255,text_rect.w + 20)
        input_rect.center = (600, 159)

        pygame.draw.rect(self.screen,(255,255,255),input_rect,2)
        self.screen.blit(text_surface,text_rect)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

if __name__ == '__main__':

    # Make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()

    

