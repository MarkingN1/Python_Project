import pygame
import random
import time
from subprocess import call

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
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Snake Game')

# Load the background image
background = pygame.image.load('INFO-Project-py/hatter2.jpg').convert()
bg_width, bg_height = background.get_size()

infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h

# Clock to control the speed of the snake
clock = pygame.time.Clock()

# Snake settings
snake_block = 30
speed_boost_duration = 10  # Duration in seconds for speed boost

font_style = pygame.font.SysFont("bahnschrift", 25)
status_font = pygame.font.SysFont("bahnschrift", 25)

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
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], snake_block, snake_block])

# Function to generate food with specified probabilities
def generate_food():
    probability = random.random()
    if probability < 0.5:  # 50% chance for red food
        food_color = red
        type = 1
    elif probability < 0.8:  # 30% chance for purple food
        food_color = purple
        type = 2
    else:  # 20% chance for pink food
        food_color = pink
        type = 3
    foodx = round(random.randrange(0, screen_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, screen_height - snake_block) / snake_block) * snake_block
    return foodx, foody, food_color, type

# Main game loop
def gameLoop():
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
    snake_speed = 10
    effect_status = "None"
    direction = 'none'
    last_input_time = 0

    foodx, foody, food_color, type = generate_food()
    foodx2, foody2 = generate_food()[:2]  # Only take the coordinates
    foodx3, foody3 = generate_food()[:2]  # Only take the coordinates

    while not game_over:

        while game_close:
            screen.fill(black)
            message = font_style.render("Game Over! Press Esc-Quit or C-Play Again", True, red)
            screen.blit(message, [screen_width // 5, screen_height // 3])
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        current_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and current_time - last_input_time >= 0.05:
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
        if type == 1:
            pygame.draw.rect(screen, food_color, [foodx, foody, snake_block, snake_block])
        elif type == 2:
            pygame.draw.rect(screen, food_color, [foodx2, foody2, snake_block, snake_block])
        else:
            pygame.draw.rect(screen, food_color, [foodx3, foody3, snake_block, snake_block])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
        display_status(effect_status)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx, foody, food_color, type = generate_food()
            Length_of_snake += 1
        if x1 == foodx2 and y1 == foody2:
            foodx2, foody2 = generate_food()[:2]  # Only take the coordinates
            Length_of_snake += 2
        if x1 == foodx3 and y1 == foody3:
            foodx3, foody3 = generate_food()[:2]  # Only take the coordinates
            Length_of_snake += 1
            is_speed_boosted = True
            speed_boost_end_time = time.time() + speed_boost_duration

        if is_speed_boosted:
            effect_status = "Faster"
            snake_speed = 20
            if time.time() >= speed_boost_end_time:
                is_speed_boosted = False
                snake_speed = 5
        else:
            effect_status = "None"

        clock.tick(snake_speed)

    pygame.quit()

gameLoop()
