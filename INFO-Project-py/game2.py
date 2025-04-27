import pygame
import random
import os
import json

pygame.init()
#music initialize
pygame.mixer.init()

music_path = "INFO-Project-py/atari_music"

music_files = [
    '1.mp3',
    '2.mp3',
    '3.mp3',
    '4.mp3',
    '5.mp3',
    '7.mp3',
    '8.mp3'
    
]
# Load the music file
#random.shuffle(music_files)
sound_files = [
    'INFO-Project-py/sound/powerupsfx.mp3'
]

def load_config():
    with open("INFO-Project-py\config.json", 'r') as f:
        return json.load(f)

def save_config(config):
    with open("INFO-Project-py\config.json", 'w') as f:
        json.dump(config, f)



# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game with Levels and Power-Ups")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_speed = 10

# Ball
BALL_RADIUS = 8
ball_speed = [4, -4]

# Bricks
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICKS_PER_ROW = 10
ROWS = 5
bricks = []

# Power-Ups
power_ups = []
POWER_UP_WIDTH, POWER_UP_HEIGHT = 40, 40

# Game State
score = 0
lives = 3
level = 1
game_over = False
paddle_expanded = False
paddle_shrink = False
invincible_ball = False
power_up_timer = 0
fast_ball = False
ball_color = RED
current_map_index = 0
maps = ["INFO-Project-py/map1.json","INFO-Project-py/map2.json"]  # List of custom maps


# Load Power-Up Icons from the "powerups" folder
icon_folder = "INFO-Project-py/powerups"
icons = {
    "bigger_paddle": pygame.image.load(os.path.join(icon_folder, "expand.png")),
    "invincible_ball": pygame.image.load(os.path.join(icon_folder, "invincible.png")),
    "extra_life": pygame.image.load(os.path.join(icon_folder, "extra_life.png")),
    "faster_ball": pygame.image.load(os.path.join(icon_folder, "fast.png")),
    "mega_ball": pygame.image.load(os.path.join(icon_folder, "mega.png")),
    "eight_ball": pygame.image.load(os.path.join(icon_folder, "eight_ball.png")),
    "shrink_paddle": pygame.image.load(os.path.join(icon_folder, "shrink.png")),
    "slow_ball": pygame.image.load(os.path.join(icon_folder, "slow.png")),
    "split_ball": pygame.image.load(os.path.join(icon_folder, "split_ball.png")),
}

# Load a map from a file
def load_custom_map(file_path):
    with open(file_path, "r") as file:
        return [{"rect": pygame.Rect(brick["x"], brick["y"], brick["width"], brick["height"]), 
                 "color": tuple(brick["color"])} for brick in json.load(file)]
# Fonts
font = pygame.font.SysFont(None, 36)

# Additional setup for multi-ball management
balls = [{"rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2), "speed": ball_speed.copy()}]

# Spawn Power-Up with Icon
def spawn_power_up(x, y):
    chance = random.random()
    if chance < 0.2:  # 10% chance to drop a power-up
        type_ = random.choice(list(icons.keys()))
        power_ups.append({
            "rect": pygame.Rect(x, y, POWER_UP_WIDTH, POWER_UP_HEIGHT),
            "type": type_,
            "icon": icons[type_]
        })

# Activate Power-Up Effects
def activate_power_up(type_):
    global paddle_expanded, invincible_ball, power_up_timer, lives, fast_ball, ball_color, paddle_shrink
    if type_ == "bigger_paddle" :
        if paddle.width < 300: 
            paddle.width += 50
            paddle_expanded = True
    elif type_ == "invincible_ball" and not invincible_ball:
        invincible_ball = True
    elif type_ == "extra_life":
        lives += 1
    elif type_ == "faster_ball" and not fast_ball:
        for ball_data in balls:
            ball_data["speed"][0] *= 1.5
            ball_data["speed"][1] *= 1.5
        fast_ball = True
    elif type_ == "mega_ball":
        for ball_data in balls:
            ball_data["rect"].width = BALL_RADIUS * 4
            ball_data["rect"].height = BALL_RADIUS * 4
        ball_color = PINK
    elif type_ == "shrink_paddle":
        if paddle.width > 50:  # Minimum paddle width
            paddle.width -= 50
            paddle_shrink = True
    elif type_ == "eight_ball":
        for _ in range(8):  # Spawn 8 additional balls
        # Generate a random direction for each new ball
            new_ball_speed = [random.choice([-4, 4]), random.choice([-4, -3, 3, 4])]
            new_ball_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
            balls.append({"rect": new_ball_rect, "speed": new_ball_speed})

    elif type_ == "split_ball":
        for ball_data in balls[:]:  # Iterate over the existing balls
        # Create a slightly varied direction for the new ball
            new_ball_speed = [-ball_data["speed"][0], ball_data["speed"][1] + random.choice([-2, 2])]
            new_ball_rect = ball_data["rect"].copy()
            balls.append({"rect": new_ball_rect, "speed": new_ball_speed})


    power_up_timer = pygame.time.get_ticks()

# Deactivate Power-Ups
def deactivate_power_ups():
    global paddle_expanded, invincible_ball, fast_ball, ball_color, paddle_shrink
    if paddle_expanded:
        paddle.width = 100
        paddle_expanded = False
    if paddle_shrink:
        paddle.width = 100
        paddle_shrink = False 
    if invincible_ball:
        invincible_ball = False
    if fast_ball:
        for ball_data in balls:
            ball_data["speed"][0] /= 1.5
            ball_data["speed"][1] /= 1.5
        fast_ball = False
    for ball_data in balls:
        ball_data["rect"].width = BALL_RADIUS * 2
        ball_data["rect"].height = BALL_RADIUS * 2
    ball_color = RED
    



def play_music():
    cfg = load_config()
    music_on = cfg['music_on']
    volume = cfg['volume']
    # Shuffle the music files to play them randomly
    random.shuffle(music_files)
    for music_file in music_files:
        music_file_path = os.path.join(music_path, music_file)
        pygame.mixer.music.load(music_file_path)  # Load the music file
        pygame.mixer.music.set_volume(volume)  # Set the volume (0.0 to 1.0)
        if music_on:
            pygame.mixer.music.play()  # Play the music in a loop (-1 for infinite loop)



def sound_effect(soundnum):
    sound_effect_up = pygame.mixer.Sound(sound_files[soundnum])
    sound_effect_up.play()  # Play the sound effect
    
# Draw Power-Ups
def draw_power_ups():
    for power_up in power_ups:
        scaled_icon = pygame.transform.scale(power_up["icon"], (POWER_UP_WIDTH, POWER_UP_HEIGHT))
        screen.blit(scaled_icon, (power_up["rect"].x, power_up["rect"].y))

# Create Bricks for Current Map
def create_bricks():
    global bricks, current_map_index
    if current_map_index < len(maps):
        bricks = load_custom_map(maps[current_map_index])
    else:
        # Victory condition when all maps are cleared
        global game_over
        game_over = True

# Restart Game
def restart_game():
    global paddle, balls, ball_speed, score, lives, level, power_ups, game_over
    paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)
    balls.clear()
    balls.append({"rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2), "speed": ball_speed.copy()})
    score = 0
    lives = 3
    level = 1
    power_ups = []
    game_over = False
    deactivate_power_ups()
    create_bricks()

# Main Game Loop
def main():
    global score, lives, level, game_over, power_up_timer

    create_bricks()
    play_music()

    running = True
    while running:
        screen.fill(BLACK)
        if (pygame.mixer_music.get_busy() == False):
            play_music()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move Paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += paddle_speed

        # Move Balls
        for ball_data in balls[:]:
            ball_rect = ball_data["rect"]
            ball_speed = ball_data["speed"]

            ball_rect.x += ball_speed[0]
            ball_rect.y += ball_speed[1]

            # Ball Collision with Walls
            if ball_rect.left <= 0 or ball_rect.right >= WIDTH:
                ball_speed[0] = -ball_speed[0]
            if ball_rect.top <= 0:
                ball_speed[1] = -ball_speed[1]

            # Ball Collision with Paddle
            # Ball Collision with Paddle
            if ball_rect.colliderect(paddle):
            # Calculate hit position relative to the paddle
             hit_position = (ball_rect.centerx - paddle.left) / paddle.width
            # Adjust ball's horizontal speed based on hit position
             ball_speed[0] = (hit_position - 0.5) * 8  # Scale to control speed range
             ball_speed[1] = -abs(ball_speed[1])  # Ensure the ball bounces upwards


           # Ball Collision with Bricks
            for brick in bricks[:]:
                if ball_rect.colliderect(brick["rect"]):
                    if invincible_ball == 0: 
                        ball_speed[1] = -ball_speed[1]
                    bricks.remove(brick)
                    score += 10
                    spawn_power_up(brick["rect"].x + brick["rect"].width // 2, brick["rect"].y + brick["rect"].height // 2)
                    break


            # Remove Ball if Out of Bounds
            if ball_rect.bottom >= HEIGHT:
                balls.remove(ball_data)
                if not balls:  # Only lose a life if no balls are left
                    lives -= 1
                    if lives > 0:
                        deactivate_power_ups()
                        new_ball = {
                            "rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2),
                            "speed": [4, -4],
                        }
                        balls.append(new_ball)
                    else:
                        game_over = True

        # Power-Up Collision with Paddle
        for power_up in power_ups[:]:
            power_up["rect"].y += 3  # Falling speed of power-ups
            if paddle.colliderect(power_up["rect"]):
                activate_power_up(power_up["type"])
                sound_effect(0)
                power_ups.remove(power_up)
            elif power_up["rect"].top > HEIGHT:
                power_ups.remove(power_up)

        # Deactivate Power-Ups after 10 seconds
        if pygame.time.get_ticks() - power_up_timer > 10000:
            deactivate_power_ups()

        # Check if Level Cleared
        if not bricks:
            level += 1
            create_bricks()
            balls.clear()
            new_ball = {
                "rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2),
                "speed": [4, -4],
            }
            balls.append(new_ball)

        # Draw Everything
        pygame.draw.rect(screen, WHITE, paddle)
        for ball_data in balls:
            pygame.draw.ellipse(screen, ball_color, ball_data["rect"])
        for brick in bricks:
            pygame.draw.rect(screen, brick["color"], brick["rect"])

        draw_power_ups()

        # Display Score, Lives, and Level
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
        screen.blit(level_text, (10, 70))

        # Display Game Over
        if game_over:
            game_over_text = font.render("Game Over! Press Esc-Quit or C-Play Again", True, YELLOW)
            screen.blit(game_over_text, (WIDTH // 5 , HEIGHT // 2))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                restart_game()
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                      

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the Game
if __name__ == "__main__":
    main()
