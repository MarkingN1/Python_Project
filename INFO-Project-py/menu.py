import pygame
import os
from subprocess import call

# Initialize Pygame
pygame.init()

# Define button colors
BUTTON_COLOR = (255, 100, 100)
BUTTON_HOVER_COLOR = (255, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Define the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Set up the font
pygame.font.init()
FONT = pygame.font.SysFont("bahnschrift", 25)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER_COLOR
        else:
            color = BUTTON_COLOR
        
        pygame.draw.rect(screen, color, self.rect)
        text_surf = FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.action()

# Define the action performed by the button (run another Pygame file)
def run_another_pygame():
 call(["python", "INFO-Project-py/game.py"])

# Create the main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Main Window')

    button = Button(300, 250, 200, 60, 'Snoke', run_another_pygame)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button.click()

        screen.fill((30, 30, 30))
        button.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
