import pygame
from subprocess import call

# Initialize Pygame
pygame.init()

# Define colors
BUTTON_COLOR = (255, 100, 100)
BUTTON_HOVER_COLOR = (255, 50, 50)
TEXT_COLOR = (255, 255, 255)
SLIDER_COLOR = (100, 100, 255)
SLIDER_BG_COLOR = (50, 50, 100)

# Define the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

running = True

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
    call(["python", "INFO-Project-py\game.py"])

def run_brick():
    call(["python", "INFO-Project-py\game2.py", str(music_on), str(volume)])

    
def exit():
    global running
    running = False

# Variables for music settings
music_on = True
volume = 0.5

def toggle_music(state):
    config.music_on = state
    if config.music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def set_volume(val):
    config.volume = val
    pygame.mixer.music.set_volume(config.volume)


def options():
    global running
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Settings')

    music_toggle = ToggleSwitch(300, 250, 200, 60, config.music_on, toggle_music)
    volume_slider = Slider(300, 350, 200, 20, 0.0, 1.0, config.volume, set_volume)
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

        screen.fill((30, 30, 30))
        music_toggle.draw(screen)
        volume_slider.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()

    if running:
        main()
        
def gamemodes():
    global running
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Select Gamemode')

    snake = Button(300, 250, 200, 60,'Snoke', run_snake )
    brick = Button(300, 320, 200, 60, 'Brick breaker',  run_brick )
    back_button2 = Button(300, 390, 200, 60, 'Back', main)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                snake.click()
                brick.click()
                back_button2.click()

        screen.fill((30, 30, 30))
        snake.draw(screen)
        brick.draw(screen)
        back_button2.draw(screen)
        pygame.display.flip()

    pygame.quit()
def main():
    global running
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Main Window')

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

        screen.fill((30, 30, 30))
        button.draw(screen)
        button2.draw(screen)
        button3.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
