import pygame
from settings import Settings

class Menu_Buttons:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))
        self.settings = Settings()
        
    def draw(self):
        pygame.draw.rect(self.settings.screen, 'dark gray', self.button, 0, 5)
        text = self.settings.menu_font.render(self.text, True, 'black')
        self.settings.screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7 ))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]: #If mouse curser is over the menu button and if the mouse is left clicked
            return True
        else:
            return False
        