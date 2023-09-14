import pygame 
from settings import Settings

pygame.init()

# Setting the frame rate to 60
fps = 60
# Assigning the clock to the timer 
timer = pygame.time.Clock()

main_menu = False
menu_command = 0

# Assigning the font to the variable font
font = pygame.font.Font('freesansbold.ttf', 24)

settings = Settings()
screen = pygame.display.set_mode((535, 500))

class Button:
    """A class to create a button"""
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))
        self.screen = settings.screen
    
    def draw(self):
        # Creating the button
        pygame.draw.rect(self.screen, 'light gray', self.button, 0, 5)
        # Creating the shadow for the button
        pygame.draw.rect(self.screen, 'dark gray', self.button, 5, 5)
        # Setting the font for the button
        text = font.render(self.text, True, 'black')
        # Setting the location for the text to display (x and y)
        self.screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        # If the mouse button is over the button and the mouse is clicked
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def draw_game():
    button = Button('Main Menu', (230, 450))
    button.draw()
    return button.check_clicked()

def draw_menu():
    """Making the menu"""
    command = 0
    pygame.draw.rect(screen, 'black', [100, 100, 300, 300])

    # Creating the exit menu button
    menu_btn = Button('Exit Menu', (120, 350))
    btn1 = Button('Button 1', (120, 180))
    btn2 = Button('Button 2', (120, 240))
    btn3 = Button('Button 3', (120, 300))

    menu_btn.draw()
    btn1.draw()
    btn2.draw()
    btn3.draw()

    if menu_btn.check_clicked():
        command = 1
    if btn1.check_clicked():
        command = 2
    if btn2.check_clicked():
        command = 3
    if btn3.check_clicked():
        command = 4

    return command

def run():
    global main_menu
    global menu_command

    run = True
    while run:
        if main_menu:
            menu_command = draw_menu()
        if menu_command > 0:
            main_menu = False
        else:
            main_menu = draw_game()
            if menu_command >= 1:
                text = font.render(f'Button {menu_command - 1} was clicked!', True, 'black')
                screen.blit(text, (100, 200))
    
        # Displays content to the screen
        pygame.display.flip()

# Call the run function to start the program
run()







