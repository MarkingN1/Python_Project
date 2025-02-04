import pygame
import random
import time  

# Initialize pygame
pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)

# Screen size
dis_width = 800
dis_height = 600

# Create the game window
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Load the background image
background = pygame.image.load('INFO-Project-py/hatter.png')

# Clock to control the speed of the snake
clock = pygame.time.Clock()

# Snake settings
snake_block = 10

speed_boost_duration = 15  # Duration in seconds for speed boost

font_style = pygame.font.SysFont("bahnschrift", 25)
status_font = pygame.font.SysFont("bahnschrift", 20)

# Function to display the score
def Your_score(score):
    value = font_style.render("Your Score: " + str(score), True, white)
    dis.blit(value, [0, 0])

# Function to display the status
def display_status(effect, time_left):
    status_text = f"Effect: {effect} | Time left: {int(time_left)}s"
    status_value = status_font.render(status_text, True, green)
    dis.blit(status_value, [dis_width / 2 - status_value.get_width() / 2, 0])

                            
# Function to draw the snake
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, purple, [x[0], x[1], snake_block, snake_block])

# Function to generate food with specified probabilities
def generate_food():
    probability = random.random()
    if probability < 0.5:  # 50% chance for red food
        food_color = red
        food_points = 1
        type=1
    elif probability < 0.8:  # 30% chance for purple food
        food_color = purple
        food_points = 2
        type=2
    else:  # 20% chance for blue food
        food_color = blue
        food_points = 1
        type=3
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    return foodx, foody, food_color, food_points, type
# Main game loop
def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    is_speed_boosted = False
    speed_boost_end_time = 0
    snake_speed = 20

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    foodx2 = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody2 = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    foodx3 = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody3 = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    direction = '.'
    foodx, foody, food_color, food_points , type = generate_food()

    while not game_over:

        while game_close:
            dis.fill(black)
            message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, red)
            dis.blit(message, [dis_width / 6, dis_height / 3])
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction!= 'RIGHT':
                    x1_change = -snake_block
                    y1_change = 0
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction!= 'LEFT':
                    x1_change = snake_block
                    y1_change = 0
                    direction = 'RIGHT'
                elif event.key == pygame.K_UP and direction!= 'DOWN':
                    y1_change = -snake_block
                    x1_change = 0
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction!= 'UP':
                    y1_change = snake_block
                    x1_change = 0
                    direction = 'DOWN'

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        
        dis.blit(background, (0, 0))  # Draw the background image
        #draw target
        if(type==1):
                    pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        elif(type==2): 
            pygame.draw.rect(dis, purple, [foodx2, foody2, snake_block, snake_block])
        else:
            pygame.draw.rect(dis, blue, [foodx3, foody3, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            foodx, foody, food_color, food_points ,type = generate_food()
        if x1 == foodx2 and y1 == foody2:
            foodx2 = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody2 = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            foodx, foody, food_color, food_points ,type = generate_food()
            Length_of_snake += 2
        if x1 == foodx3 and y1 == foody3:
            foodx3 = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody3 = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            foodx, foody, food_color, food_points ,type = generate_food()
            Length_of_snake += 1
            is_speed_boosted = True
            speed_boost_end_time = time.time() + speed_boost_duration
        
        if is_speed_boosted:
            snake_speed = 30
            if time.time() >= speed_boost_end_time:
                is_speed_boosted = False
                snake_speed = 20
        clock.tick(snake_speed)
        if is_speed_boosted:
            display_status("Faster", speed_boost_end_time - time.time())
        else:
            display_status("None", 0)
        

    pygame.quit()
    quit()

gameLoop()