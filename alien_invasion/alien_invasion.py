import sys
import pygame 
import time
import random

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from music import Music
from menu_buttons import Menu_Buttons
pygame.init()



main_menu = False




class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock() #Defining the clock that sets the frame rate for the game
        self.settings = Settings() #We create an instance of settings and assign it to self.settings
        
        self.screen = self.settings.screen
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        #Attribute to keep track of the power-up start time
        self.power_up_start_time = None

        #Setting the caption name for the program 
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game sounds 
        self.sounds = Music(self)
        
        #Create an instance to store game statistics and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self) #Here we assign an instance of the Ship class to self.ship
        self.bullets = pygame.sprite.Group() #This stores the bullets
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
    
        #Set the background color
        self.bg_color = (230, 230, 230) #Setting the color value for the background color

        #Start Alien Invasion in an inactive state
        self.game_active = False

        #Make the play button 
        self.play_button = Button(self, "Play")


        #Setting the powerup loop to false
        self.score_already_thousand = False

        #Setting the power up button to false
        self.power_up_button = False

        self.main_menu = False

        self.menu_command = 0

        #Create an instance of the bullet class 
        self.bullet_class = Bullet(self)



   

        


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            #If the game is active
            if self.game_active:
             self.ship.update()
             self._update_bullets()
             self._update_aliens()
             self.bullet_power_up()
            


             
            self._update_screen()
            self.clock.tick(60) #This is the set frame rate for the game (60 times per second)
    
    def _update_bullets(self):
        """Update the position of bullets and get rid of the old bullets"""
        #Update bullet positions
        self.bullets.update() 
        self.bullet_power_up()
        #Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisons()

    def _check_bullet_alien_collisons(self):
        """Respond to bullet-alien collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
             self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sounds.alien_shoot.play()
        if not self.aliens:
            #Destory existing bullets and create a new fleet 
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase Level
            self.stats.level += 1
            self.sb.prep_level()

         


    def bullet_power_up(self):
        """Make a bullet power-up"""

        current_time = pygame.time.get_ticks()
        if self.stats.score == 1000 and not self.settings.bullet_power_up and not self.score_already_thousand:
            self.sounds.power_up_available_sound.play(+1)
        #Executes the bullet powerup if the conditions are met
        if self.stats.score >= 1000 and not self.settings.bullet_power_up and not self.score_already_thousand and self.power_up_button == True:
            self.score_already_thousand = True #Stops this if statement looping if the powerup has already been activiated at 1000 score
            self.settings.bullet_power_up = True
            self.settings.bullet_width = 6
            self.settings.bullet_height = 30
            self.settings.bullet_color = (255, 255, 0)
            self.settings.bullet_allowed = 3
            self.sounds.shoot_sound = pygame.mixer.Sound('alien_invasion/music/bullet_power_up.wav')
            self.power_up_start_time = current_time
            self.power_up_image = pygame.image.load('alien_invasion/images/power_up.jpg')
            self.screen.blit(self.power_up_image, (200, 150))

        


        #Reverting the bullet to its original state once the power up has ended
        if self.settings.bullet_power_up == True and current_time - self.power_up_start_time >=10000:
         self.settings.bullet_width = 3
         self.settings.bullet_height = 15
         self.settings.bullet_color = (255, 0, 0)
         self.settings.bullet_allowed = 3
         self.sounds.shoot_sound = pygame.mixer.Sound('alien_invasion/music/sounds_shoot.wav')
         

           

    


    def _update_aliens(self):
        """CHeck if the fleet is at an edge, then update positions"""
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()
    

    def _create_fleet(self):
        """Create the fleet of aliens"""
        #Create an alien and keep adding aliens until there is no room left
        #Spacing between aliens is one alien width and one alien height
        self.alien_image_change()
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        self.sounds.new_fleet_sound.play()
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
             #Finished a row; reset x value, and increment y value 
            current_x = alien_width
            current_y += 2 * alien_height

    def alien_image_change(self):
        #Changes the image of the alien if the set level is reached
        self.alien_class = Alien(self)
        if self.stats.level >= 3:
            self.alien_class.image = pygame.image.load('alien_invasion/images/alien2.png')
            

        else:
            self.alien_class.image = pygame.image.load('alien_invasion/images/alien.png')

        


    def _create_alien(self, x_position, y_position):
        #Create an alien and place it in the fleet
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        self.alien_image_change()





    def _check_fleet_edges(self):
        """Respond approprietly if any aliens have reached the edge of the screen"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        if self.stats.ships_left > 0:
         #Decrement ships left and update scoreboard
         self.stats.ships_left -= 1
         self.sb.prep_ships()

         #Get rid of any remaining bullets and aliens
         self.bullets.empty()
         self.aliens.empty()

         #Create a new fleet and center the ship 
         self._create_fleet()
         self.ship.center_ship()

         #Play the ship destroyed sound if the ship is hit
         self.sounds.ship_destroyed_sound.play()

         #Pause
         time.sleep(1.0) # Pausing the game when the player is hit so that they have time to notice the game reset
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        #Redraw the screen during each pass through the loop
            self.screen.blit(self.settings.bg, (0, 0)) #The fill method allows us to fill the background with the color we have chosen
    
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme() #Draws the ship on the screen
            self.aliens.draw(self.screen) # Draws the aliens onto the screen

            #Draw the score information
            self.sb.show_score()

            #Draw the play button if the game is inactive
            if not self.game_active:
                self.play_button.draw_button()
            
            #Draw the power up image if the power up is available
            self.bullet_power_up()
            
            #Draw the new alien if the image has changed
            self.alien_image_change()



  

            # Make the most recently drawn screen visible
            pygame.display.flip() 

    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                self.mute_sounds(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
           


            
    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.

    
             
            
    def mute_sounds(self, event):
     """Mute sounds when the m key is pressed"""
     if event.key == pygame.K_m:
        if self.sounds.shoot_sound.get_volume() > 0:
            # Sound is currently unmuted, so mute it
            self.sounds.shoot_sound.set_volume(0)
            self.sounds.ship_destroyed_sound.set_volume(0)
            self.sounds.new_fleet_sound.set_volume(0)
            self.sounds.alien_shoot.set_volume(0)
            self.sounds.power_up_available_sound.set_volume(0)

  
        else:
            # Sound is currently muted, so unmute it
            self.sounds.shoot_sound.set_volume(1)
            self.sounds.new_fleet_sound.set_volume(1)
            self.sounds.ship_destroyed_sound.set_volume(1)
            self.sounds.alien_shoot.set_volume(1)
            self.sounds.power_up_available_sound.set_volume(1)
            

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE or event.key == pygame.K_w:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self.power_up_button = True
            
    
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key ==pygame.K_a:
            self.ship.moving_left = False
        
        
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullet_allowed:
         new_bullet = Bullet(self)
         self.bullets.add(new_bullet)
         self.sounds.shoot_sound.play()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Treat this the same as if the ship got hit 
                self._ship_hit()
                break
     
    def draw_menu_button(self):
        """Creates and draws the menu button at the coordinates specified"""
        button = Menu_Buttons('Main Menu', (230, 450))
        button.draw()
        return button.check_clicked()

        

    def draw_menu(self):
        command = 0
        pygame.draw.rect(self.settings.screen, 'yellow', [100, 100, 300, 300])
        #Exit menu button
        menu_btn = Menu_Buttons('Exit Menu',(120, 350))

        #Making the buttons
        btn1 = Menu_Buttons('Button 1',(120, 180))
        btn2 = Menu_Buttons('Button 2',(120, 240))
        btn3 = Menu_Buttons('Button 3',(120, 300))
        menu_btn.draw()

        #Draw the buttons onto the screen
        btn1.draw()
        btn2.draw()
        btn3.draw()

        #Giving each button a command
        if menu_btn.check_clicked():
          command = 1
        if btn1.check_clicked():
            command = 2
        if btn2.check_clicked():
            command = 3
        if btn3.check_clicked():
            command = 4

        return command
    
    

if __name__ == '__main__':
    #Make a game instance and run the game.
    ai = AlienInvasion()
    ai.run_game()
