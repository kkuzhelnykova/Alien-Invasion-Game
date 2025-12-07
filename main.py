import sys

from time import sleep
import pygame

from button import Button
from bullet import Bullet
from game_stats import GameStats
from settings import Settings
from ship import Ship
from alien import Alien

class AlienInvasion:
    #Overall class to manage game assets and behavior
    
    def __init__(self):
        #Initialize the game, and create game resources
        
        pygame.init()
        self.settings = Settings ()
        
        self.screen = pygame.display.set_mode ((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Kuzhelnykova's Alien Invasion")

        #Create an instance to store game statistics
        self.stats = GameStats(self)
        
        # Set the background color - colors are RBG colors: amix of red, green,and blue. Each color range is o to 255
        self.bg_color = (200, 190, 250)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Add in the alien
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #if the game is paused
        self.game_paused = False
        continue_image = pygame.image.load("Images/continue.png")
        quit_image = pygame.image.load("Images/quit.png")
        new_game_image = pygame.image.load("Images/newGame.png")
        self.continue_button = Button(self.settings.screen_width/2,self.settings.screen_height/4, continue_image,0.7,self)
        self.new_game_button = Button(self.settings.screen_width/2,(self.settings.screen_height/4)*2,new_game_image,0.7,self)
        self.quit_button = Button(self.settings.screen_width/2,(self.settings.screen_height/4)*3,quit_image,0.6,self)
        
        #Button to show status on top left
        self.kill_count = 0

    def run_game(self):
        #Start the main loop for the game
        
        while True:
           # call a method to check to see if any keyboard events have occurred
            self._check_events() 
            if self.game_paused:
                self._paused()
            else:
                #Check if the game is active before updating the ship, bullets, and aliens
                if self.stats.game_active:
                    self.ship.update()
                    self._update_bullets()
                    self._update_aliens()
                    self._update_screen()
                else:
                    self.screen.fill(self.bg_color)
                    black = (0, 0, 0)
                    font = pygame.font.Font(None, 100)
                    text = font.render(f'YOU LOST ', True, black)
                    text_rect = text.get_rect(center = pygame.display.get_surface().get_rect().center)
                    self.screen.blit(text, text_rect)
                    pygame.display.flip()
            
    def _paused(self):
        self.screen.fill(self.settings.bg_color)
        if self.continue_button.draw():
            self.game_paused = False
        if self.quit_button.draw():
            sys.exit()
        if self.new_game_button.draw():
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.stats.reset_stats()
            self.kill_count = 0
            self.ship.center_ship()          # (optional but nice)
            self.stats.game_active = True    # <-- IMPORTANT
            self.game_paused = False         # back to playing
        pygame.display.flip()

    
    def _check_events(self):
        #Respond to keypresses and mouse events.
        # Did the player quit the game?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Did the player press the right or left arrow key?
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            # Did the player stop holding down the arrow key?
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Right/left movement
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        # Quit the game with Q
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

        # Fire bullets only when not paused and game is active
        elif event.key == pygame.K_SPACE and self.stats.game_active and not self.game_paused:
            self._fire_bullet()

        # Toggle pause with P
        elif event.key == pygame.K_p:
            self.game_paused = not self.game_paused
            print("Paused:", self.game_paused)  # debug text in terminal



    def _check_keyup_events(self, event):
        # Did the player stop holding down the arrow keys?
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self):
        #Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        #Update position of bullets and get rid of old bullets
        #Update bullet positions
        self.bullets.update()
        
        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
    
    def _check_bullet_alien_collisions(self):
        #Respond to bullet-alien collisions
        #Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            self.kill_count += 1

        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        #Update the positions of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("SHIP HIT!!!")
            self._ship_hit()
        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    #Add a method to create the fleet of aliens
    def _create_fleet(self):
        #Create the fleet of aliens
        # Make a single alien.
        aliens = Alien(self)
        alien_width, alien_height = aliens.rect.size
        
        # Determine how much space you have on the screen for aliens
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        #Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Create the full fleet of aliens
        for row_number in range (number_rows):
            for alien_number in range (number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        #Respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #Drop the entire fleet and change the fleet's direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        #Respond to the ship being hit by an alien
        
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update the scoreboard
            self.stats.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            self.game_paused = True 
        
    def _check_aliens_bottom(self):
        #Check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        #Update images on the screen, and flip to the new screen.
        # Redraw the screen each pass through the 1oop
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        # Draw the alien
        self.aliens.draw(self.screen)

        #Show status on display
        black = (0, 0, 0)
        font = pygame.font.SysFont('Papyrus', 42)
        text = font.render(f'Ships left: {self.stats.ships_left}', True, black)
        textRect = text.get_rect()
        textRect.center = (250 // 2, 100 // 2)
        self.screen.blit(text, textRect)
        text = font.render(f'Aliens hit: {self.kill_count}', True, black)
        textRect = text.get_rect()
        textRect.center = (250 // 2, 200 // 2)
        self.screen.blit(text,textRect)

        # Make the most recently drawn screen visible
        pygame.display.flip() 
        
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()

quit()