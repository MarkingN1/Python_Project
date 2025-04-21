import pygame
import random
import time
from subprocess import call
import os

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)
pink = (255, 111, 246)

# Create the game window
screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption('Snake Game')

# Load the background image
background = pygame.image.load('INFO-Project-py/hatter2.jpg').convert()
bg_width, bg_height = background.get_size()

infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

okblock = screen_height
# Clock to control the speed of the snake
clock = pygame.time.Clock()

# Snake settings
snake_speed = 8
snake_block = 20
speed_boost_duration = 3  # Duration in seconds for speed boost

font_style = pygame.font.SysFont("bahnschrift", 25)
status_font = pygame.font.SysFont("bahnschrift", 25)


icon_folder = "INFO-Project-py/snake"
icons = {
    "apple": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "alma.png")), (snake_block, snake_block)),
    "plum": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "plum.png")), (snake_block, snake_block)),
    "pepper": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "pepper.png")), (snake_block, snake_block)),
    "pear": pygame.transform.scale(pygame.image.load(os.path.join(icon_folder, "korte.png")), (snake_block, snake_block)),
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



# Function to display the score
def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    screen.blit(value, [0, 0])

# Function to display the status
def display_status(effect):
    status_text = "Effect: "
    status_value = status_font.render(status_text + str(effect), True, red)
    screen.blit(status_value, [0, 25])

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
def generate_food():
    probability = random.random()
    if probability < 0.5:  # 50% chance for red food
        type = "apple"
        score = 1
    elif probability < 0.8:  # 30% chance for purple food
        type = "plum"
        score = 2
    else:  # 20% chance for pink food
        type = "pepper"
        score = 3
    foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
    return foodx, foody, type, score


# Main game loop
def gameLoop():
    global snake_speed
    game_over = False
    game_close = False

    x1 = 300
    y1 = 300

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    is_speed_boosted = False
    speed_boost_end_time = 0
    effect_status = "NONE"
    direction = 'RIGHT'
    last_input_time = 0

    foodx, foody, type, score = generate_food()

    while not game_over:

        while game_close:
            screen.fill(black)
            message = font_style.render("Game Over! Press Esc-Quit or SPACE-Play Again", True, red)
            screen.blit(message, [screen_width // 5, screen_height // 3])
            Your_score(Length_of_snake)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_SPACE:
                        gameLoop()

        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and current_time - last_input_time >= 0.02:
                last_input_time = current_time
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

        if x1 >= screen_width or x1 < 0 or y1 >= screen_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Draw the background image
        for x in range(0, screen_width, bg_width):
            for y in range(0, screen_height, bg_height):
                screen.blit(background, (x, y))

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

        our_snake(snake_List,direction)
        Your_score(Length_of_snake - 1)
        display_status(effect_status)
        pygame.display.update()
        
        if x1==foodx and y1==foody:
             if type == "apple":
                Length_of_snake += score
             elif type == "plum":
                Length_of_snake += score
             elif type == "pepper":
                Length_of_snake += score
                is_speed_boosted = True
                speed_boost_end_time = time.time() + speed_boost_duration
             foodx, foody, type, score = generate_food()

        if is_speed_boosted:
            effect_status = "Faster"
            snake_speed = 12
            if time.time() >= speed_boost_end_time:
                is_speed_boosted = False
                snake_speed = 8
        else:
            effect_status = "None"

        clock.tick(snake_speed)

    pygame.quit()

gameLoop()
