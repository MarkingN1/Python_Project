import pygame
import random
import time
import os
import json

# Initialize pygame
pygame.init()

# Colors
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
TEAL =  (0, 0, 128)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

# Create the game window
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption('Snake Game')

# Load the background image
BACKGROUND = pygame.image.load('INFO-Project-py/BackGround/hatter2ok.jpg').convert()
BG_WIDTH, BG_HEIGHT = BACKGROUND.get_size()

clock = pygame.time.Clock()


MUSIC_PATH = "INFO-Project-py/atari_music"

MUSIC_FILES = [
    '1.mp3',
    '2.mp3',
    '3.mp3',
    '4.mp3',
    '5.mp3',
    '7.mp3',
    '8.mp3'
    
]


# Snake settings
snake_speed = 8
snake_block = 30  #30
speed_boost_duration = 3  # Duration in seconds for speed boost
personal_best = 0

food_spawn_time = 0
food_lifetime = 5  # Lifetime of food in seconds


FONT_STYLE = pygame.font.SysFont("bahnschrift", 25)
STATUS_FONT = pygame.font.SysFont("bahnschrift", 25)

#Grapthic imports 
icon_folder = "INFO-Project-py/Images"
icons = {
    "apple": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "apple.png")), (snake_block, snake_block)),
    "banana": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "banana.png")), (snake_block, snake_block)),
    "plum": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "plum.png")), (snake_block, snake_block))
}        

snake_graphics = "INFO-Project-py/Graphics"
direction_icons = {
        "head_up": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "head_up.png")), (snake_block, snake_block)),
        "head_down": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "head_down.png")), (snake_block, snake_block)),
        "head_right": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "head_right.png")), (snake_block, snake_block)),
        "head_left": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "head_left.png")), (snake_block, snake_block)),
        "body_vertical": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "body_vertical.png")), (snake_block, snake_block)),
        "body_horizontal": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "body_horizontal.png")), (snake_block, snake_block)),
        "body_topright": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "body_topright.png")), (snake_block, snake_block)),
        "body_topleft": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "body_topleft.png")), (snake_block, snake_block)),
        "body_bottomleft": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "body_bottomleft.png")), (snake_block, snake_block)),
        "body_bottomright": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "body_bottomright.png")), (snake_block, snake_block)),
        "tail_up": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "tail_up.png")), (snake_block, snake_block)),
        "tail_down": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "tail_down.png")), (snake_block, snake_block)),
        "tail_right": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "tail_right.png")), (snake_block, snake_block)),
        "tail_left": pygame.transform.scale(pygame.image.load(os.path.join(snake_graphics, "tail_left.png")), (snake_block, snake_block)),
}





def load_config():
    with open("INFO-Project-py\config.json", 'r') as f:
        return json.load(f)

def save_config(config):
    with open("INFO-Project-py\config.json", 'w') as f:
        json.dump(config, f)

def play_music():
    cfg = load_config()
    music_on = cfg['music_on']
    volume = cfg['volume']
    random.shuffle(MUSIC_FILES)
    for music_file in MUSIC_FILES:
        music_file_path = os.path.join(MUSIC_PATH, music_file)
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.set_volume(volume)  
        if music_on:
            pygame.mixer.music.play() 
            
def save_personal_best(personal_best):
    cfg = load_config()
    cfg['personal_best'] = personal_best
    save_config(cfg)
    
    
    
# Function to display on the screen
def Your_score(score):
    value = FONT_STYLE.render("Your Score: " + str(score), True, TEAL)
    screen.blit(value, [0, 0])
    
def display_personal_best(best_score):
    best_text = FONT_STYLE.render(f"Personal Best: {best_score}", True, PURPLE)
    screen.blit(best_text, [0, 25])

def display_status(effect):
    status_text = "Effect: "
    status_value = STATUS_FONT.render(status_text + str(effect), True, RED)
    screen.blit(status_value, [0, 50])

def display_messages(remaining_time):
    just_text = FONT_STYLE.render(f"Food timer: {int(remaining_time)} seconds", True, BLACK)
    screen.blit(just_text, [0, 75])


# Function to draw the snake
def our_snake(snake_list, direction):
    for i, x in enumerate(snake_list):
        if i == len(snake_list) - 1:
            # Draw the head
            if direction == "UP":
                screen.blit(direction_icons["head_up"], (x[0], x[1]))
            elif direction == "DOWN":
                screen.blit(direction_icons["head_down"], (x[0], x[1]))
            elif direction == "RIGHT":
                screen.blit(direction_icons["head_right"], (x[0], x[1]))
            elif direction == "LEFT":
                screen.blit(direction_icons["head_left"], (x[0], x[1]))
        elif i == 0:
            # Draw the tail
            if len(snake_list) > 1: 
                next_segment = snake_list[i + 1] 
                if next_segment[0] == x[0]: 
                    if next_segment[1] > x[1]:  
                        screen.blit(direction_icons["tail_up"], (x[0], x[1]))
                    else:
                        screen.blit(direction_icons["tail_down"], (x[0], x[1]))
                elif next_segment[1] == x[1]:  
                    if next_segment[0] > x[0]: 
                        screen.blit(direction_icons["tail_left"], (x[0], x[1]))
                    else: 
                        screen.blit(direction_icons["tail_right"], (x[0], x[1]))
        else:
            # Draw the body
            prev_segment = snake_list[i - 1]
            next_segment = snake_list[i + 1]

            if prev_segment[0] == x[0] and next_segment[0] == x[0]:
                # Vertical body
                screen.blit(direction_icons["body_vertical"], (x[0], x[1]))
            elif prev_segment[1] == x[1] and next_segment[1] == x[1]:
                # Horizontal body
                screen.blit(direction_icons["body_horizontal"], (x[0], x[1]))
            else:
                # Determine corners
                if prev_segment[0] < x[0] and next_segment[1] < x[1]:
                    screen.blit(direction_icons["body_topleft"], (x[0], x[1]))
                elif prev_segment[1] < x[1] and next_segment[0] < x[0]:
                    screen.blit(direction_icons["body_topleft"], (x[0], x[1]))
                    
                elif prev_segment[0] > x[0] and next_segment[1] < x[1]:
                    screen.blit(direction_icons["body_topright"], (x[0], x[1]))
                elif prev_segment[1] < x[1] and next_segment[0] > x[0]:
                    screen.blit(direction_icons["body_topright"], (x[0], x[1]))
                    
                elif prev_segment[0] < x[0] and next_segment[1] > x[1]:
                    screen.blit(direction_icons["body_bottomleft"], (x[0], x[1]))
                elif prev_segment[1] > x[1] and next_segment[0] < x[0]:
                    screen.blit(direction_icons["body_bottomleft"], (x[0], x[1]))
                    
                elif prev_segment[0] > x[0] and next_segment[1] > x[1]:
                    screen.blit(direction_icons["body_bottomright"], (x[0], x[1]))
                elif prev_segment[1] > x[1] and next_segment[0] > x[0]:
                    screen.blit(direction_icons["body_bottomright"], (x[0], x[1]))
                


# Function to generate food with specified probabilities
def generate_food(snake_list):
    while True:
        probability = random.random()  # Generate a random number between 0 and 1
        if probability < 0.5:  # 60% chance for apple
            type = "apple"
            score = 1
        elif probability < 0.8:  # 20% chance for plum (0.7 to 0.9)
            type = "plum"
            score = 2
        else:  # 10% chance for banana (0.9 to 1.0)
            type = "banana"
            score = 3
        foodx = round(random.randrange(90, SCREEN_WIDTH - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(60, SCREEN_HEIGHT - snake_block) / snake_block) * snake_block

        # Check if the food overlaps with the snake
        if [foodx, foody] not in snake_list:
            break  # Exit the loop if the food does not overlap

    return foodx, foody, type, score


# Main game loop
def gameLoop():
    global snake_speed
    global food_spawn_time
    global snake_speed
    global personal_best
    game_over = False
    game_close = False
    x1 = 300
    y1 = 300

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    snake_speed = 8
    snake_block = 30
    is_speed_boosted = False
    speed_boost_end_time = 0
    slow_speed = False
    slow_speed_end_time = 0
    effect_status = "NONE"
    direction = 'RIGHT'
    last_input_time = 0
    cfg = load_config()
    personal_best = cfg['personal_best']
    

    foodx, foody, type, score = generate_food(snake_List)
    
    play_music()

    while not game_over:
    
        screen.fill((0,0,0))
        while game_close:
            screen.fill(BLACK)
            message = FONT_STYLE.render("Game Over! Press Esc-Quit or SPACE-Play Again", True, RED)
            screen.blit(message, [SCREEN_WIDTH // 5, SCREEN_HEIGHT // 3])
            Your_score(Length_of_snake)
            display_personal_best(personal_best)
            save_personal_best(personal_best)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop()

        current_time = time.time()
        
        if (pygame.mixer_music.get_busy() == False):
            play_music()
    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and current_time - last_input_time >= 0.02:
                last_input_time = current_time
                if x1 < SCREEN_WIDTH and y1 < SCREEN_HEIGHT and y1 >= 0 and x1 >= 0:
                    if event.key == pygame.K_LEFT and direction != 'RIGHT':
                        x1_change = -snake_block
                        y1_change = 0
                        direction = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        x1_change = snake_block
                        y1_change = 0
                        direction = 'RIGHT'
                    elif event.key == pygame.K_UP and direction != 'DOWN':
                        y1_change = -snake_block
                        x1_change = 0
                        direction = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        y1_change = snake_block
                        x1_change = 0
                        direction = 'DOWN'
                    elif event.key == pygame.K_ESCAPE:
                        game_close = False
                        game_over = True
       
           
         # Wall Teleportation mechanism
        if x1 >= SCREEN_WIDTH:
            x1 = 0 - snake_block    # Wrap around to the left side
        elif x1 < 0:
            x1 = SCREEN_WIDTH # Wrap around to the right side
        elif y1 >= SCREEN_HEIGHT:
            y1 = 0 - snake_block # Wrap around to the top
        elif y1 < 0:
            y1 = SCREEN_HEIGHT  # Wrap around to the bottom 
                
        x1 += x1_change
        y1 += y1_change
            
        # Calculate remaining time for the food
        remaining_time = max(0, food_lifetime - (time.time() - food_spawn_time)+1)

        

        # Draw the background image
        for x in range(0, SCREEN_WIDTH, BG_WIDTH):
            for y in range(0, SCREEN_HEIGHT, BG_HEIGHT):
                screen.blit(BACKGROUND, (x, y))

        # Draw target
                  # Draw food icon
        if type in icons:
            screen.blit(icons[type], (foodx, foody))  # Use the corresponding icon image
            

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
            
            
        #Self Collision mechanism
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
                pygame.mixer_music.stop()
                
        if Length_of_snake > personal_best:
            personal_best = Length_of_snake
         
                
        our_snake(snake_List,direction)
        Your_score(Length_of_snake)
        display_status(effect_status)
        display_messages(remaining_time)
        display_personal_best(personal_best)    
        pygame.display.update()
        
        if time.time() - food_spawn_time > food_lifetime:
            foodx, foody, type, score = generate_food(snake_List)
            food_spawn_time = time.time()  # Reset the timer for the new food

        
        
        if x1 == foodx and y1 == foody:
            if type == "apple":
                Length_of_snake += score
            elif type == "plum":
                Length_of_snake += score
                slow_speed = True
                slow_speed_end_time = time.time() + speed_boost_duration
            elif type == "banana":
                Length_of_snake += score
                is_speed_boosted = True
                speed_boost_end_time = time.time() + speed_boost_duration
            foodx, foody, type, score = generate_food(snake_List)
            food_spawn_time = time.time()  # Reset the timer for the new food


        if is_speed_boosted:
            effect_status = "Faster"
            snake_speed = 12
            if time.time() >= speed_boost_end_time:
                is_speed_boosted = False
                snake_speed = 8
                
            #Slow effect Implementation
        elif slow_speed:
            effect_status = "Slowed"
            snake_speed = 4
            if time.time() >= slow_speed_end_time:
                slow_speed = False
                snake_speed = 8
        else:
            effect_status = "NONE"        
            
        clock.tick(snake_speed)
        pygame.display.update()

    pygame.quit()

gameLoop()
