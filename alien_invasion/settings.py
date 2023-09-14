import pygame
class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen =  pygame.display.set_mode((535, 500))
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.bg = pygame.image.load('alien_invasion/images/background2.jpg')
        
        self.bullet_power_up = False

        #Ship settings
        self.ship_limit = 3 #Settings the value of the amount of ship lives a player gets 

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 3
            
        #Alien settings
        self.fleet_drop_speed = 10

        #How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        #Text for the menu 
        self.menu_font = pygame.font.Font('freesansbold.ttf', 24)

    def initialize_dynamic_settings(self):
        """Initialize settings thta change throughout the game"""
        self.ship_speed = 2.0
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        #Fleet direction of 1 represents right; -1 represents left 
        self.fleet_direction = 1

        #Scoring settings
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
    



        
        

        

        