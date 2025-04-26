import pygame
from subprocess import call
import json

# Initialize Pygame
pygame.init()


# Define colors
BUTTON_COLOR = (255, 100, 100)
BUTTON_HOVER_COLOR = (255, 50, 50)
TEXT_COLOR = (255, 255, 255)
SLIDER_COLOR = (100, 100, 255)
SLIDER_BG_COLOR = (50, 50, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
PURPLE = (128, 0, 128)
PINK = (255, 111, 246)
YELLOW = (255, 232, 31)
ORANGE = (255,127,80)
ORANGEL = (255,165,0)

# Define the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Window')


music_path = "INFO-Project-py/sound/lofi.mp3"

BACKGROUND = pygame.image.load('INFO-Project-py/BackGround/bg2.jpg').convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

def load_config():
    with open("INFO-Project-py\config.json", 'r') as f:
        return json.load(f)

def save_config(config):
    with open("INFO-Project-py\config.json", 'w') as f:
        json.dump(config, f)


running = True

# Set up the font
pygame.font.init()
FONT = pygame.font.SysFont("Avenir", 30)

pygame.mixer_music.load(music_path)
pygame.mixer_music.play()

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = ORANGE
        else:
            color = ORANGEL
        
        pygame.draw.rect(screen, color, self.rect)
        text_surf = FONT.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.action()

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.callback = callback
        self.dragging = False

    def draw(self, screen):
        pygame.draw.rect(screen, SLIDER_BG_COLOR, self.rect)
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 10, self.rect.y, 20, self.rect.height)
        pygame.draw.rect(screen, SLIDER_COLOR, handle_rect)
        volume_text = FONT.render(f"Volume: {int(self.value * 100)}%", True, TEXT_COLOR)
        volume_text_rect = volume_text.get_rect(center=(self.rect.centerx, self.rect.y - 20))
        screen.blit(volume_text, volume_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                rel_x = event.pos[0] - self.rect.x
                self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
                self.value = max(self.min_val, min(self.value, self.max_val))
                self.callback(self.value)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                rel_x = event.pos[0] - self.rect.x
                self.value = self.min_val + (rel_x / self.rect.width) * (self.max_val - self.min_val)
                self.value = max(self.min_val, min(self.value, self.max_val))
                self.callback(self.value)

class ToggleSwitch:
    def __init__(self, x, y, width, height, initial_state, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.state = initial_state
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR if self.state else BUTTON_HOVER_COLOR, self.rect)
        text_surf = FONT.render("On" if self.state else "Off", True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        label_text = FONT.render("Music", True, TEXT_COLOR)
        label_rect = label_text.get_rect(center=(self.rect.centerx, self.rect.y - 20))
        screen.blit(label_text, label_rect)

    def click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.state = not self.state
            self.callback(self.state)

def run_snake():
    pygame.mixer_music.stop()
    call(["python", "INFO-Project-py\game.py"])

def run_brick():
    pygame.mixer_music.stop()
    call(["python", "INFO-Project-py\game2.py"])

    
def exit():
    global running
    running = False

# Variables for music settings
music_on = True
volume = 0.5

def toggle_music(state):
    
    cfg = load_config()
    cfg['music_on'] = state
    save_config(cfg)
    if(state):
        pygame.mixer_music.play()
    else:
        pygame.mixer_music.stop() 
        
def draw_title(screen, text, y_position):
    """Draw a title at the top of the screen."""
    title_surface = FONT.render(text, True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, y_position))
    screen.blit(title_surface, title_rect)
    

def set_volume(val):
    cfg = load_config()
    cfg['volume'] = val
    save_config(cfg)
    pygame.mixer.music.set_volume(val)


def options():
    cfg = load_config()
    global running
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Settings')

    music_toggle = ToggleSwitch(300, 250, 200, 60, cfg['music_on'], toggle_music)
    volume_slider = Slider(300, 350, 200, 20, 0.0, 1.0, cfg['volume'], set_volume)
    back_button = Button(300, 390, 200, 60, 'Back', main)

    options_running = True
    while options_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                options_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                music_toggle.click()
                back_button.click()
                volume_slider.handle_event(event)
            elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
                volume_slider.handle_event(event)

        screen.blit(BACKGROUND, (0, 0))
        music_toggle.draw(screen)
        volume_slider.draw(screen)
        back_button.draw(screen)
        pygame.display.update()

    if running:
        main()
        
def gamemodes():
    global running
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Select Gamemode')
    snake = Button(300, 250, 200, 60,'Snoke', run_snake)
    brick = Button(300, 320, 200, 60, 'Brick breaker',  run_brick )
    back_button2 = Button(300, 390, 200, 60, 'Back', main)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                snake.click()
                pygame.mixer_music.stop
                brick.click()
                pygame.mixer_music.stop
                back_button2.click()

        screen.blit(BACKGROUND, (0, 0))
        snake.draw(screen)
        brick.draw(screen)
        back_button2.draw(screen)
        pygame.display.flip()

    pygame.quit()
def main():
    global running

    button = Button(300, 250, 200, 60, 'Select gamemode', gamemodes )
    button2 = Button(300, 390, 200, 60, 'Exit', exit )
    button3 = Button(300, 320, 200, 60, 'Options', options )
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button.click()
                button2.click()
                button3.click()

        screen.blit(BACKGROUND, (0, 0))
        
        
        draw_title(screen, "Arcade Games Offline", 100)
        
        button.draw(screen)
        button2.draw(screen)
        button3.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
