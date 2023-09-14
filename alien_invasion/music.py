import pygame
class Music:
    """A class to store all of the game sounds"""

    def __init__(self, ai_game):
       
         self.shoot_sound = pygame.mixer.Sound('alien_invasion/music/sounds_shoot.wav')
         self.ship_destroyed_sound = pygame.mixer.Sound('alien_invasion/music/shipexplosion.wav')
         self.new_fleet_sound = pygame.mixer.Sound('alien_invasion/music/new_fleet.wav')
         self.alien_shoot = pygame.mixer.Sound('alien_invasion/music/alienshoot.ogg')
         self.power_up_available_sound = pygame.mixer.Sound('alien_invasion/music/power_up_available.wav')



         
         

