import pygame
import random
import os

# Initialize Pygame
pygame.init()

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
paddle_speed = 7

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
invincible_ball = False
power_up_timer = 0
fast_ball = False
ball_color = RED


# Load Power-Up Icons from the "powerups" folder
icon_folder = "powerups"
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

# Fonts
font = pygame.font.SysFont(None, 36)

# Additional setup for multi-ball management
balls = [{"rect": pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2), "speed": ball_speed.copy()}]

# Spawn Power-Up with Icon
def spawn_power_up(x, y):
    chance = random.random()
    if chance < 0.3:  # 30% chance to drop a power-up
        type_ = random.choice(list(icons.keys()))
        power_ups.append({
            "rect": pygame.Rect(x, y, POWER_UP_WIDTH, POWER_UP_HEIGHT),
            "type": type_,
            "icon": icons[type_]
        })

# Activate Power-Up Effects
def activate_power_up(type_):
    global paddle_expanded, invincible_ball, power_up_timer, lives, fast_ball, ball_color
    if type_ == "bigger_paddle" and not paddle_expanded:
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
    elif type_ == "eight_ball":
        for _ in range(8):  # Spawn 8 additional balls
            new_ball_speed = [random.choice([-4, 4]), random.choice([-4, 4])]
            new_ball_rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
            balls.append({"rect": new_ball_rect, "speed": new_ball_speed})
    elif type_ == "shrink_paddle":
        if paddle.width > 50:  # Minimum paddle width
            paddle.width -= 50
    elif type_ == "slow_ball":
        for ball_data in balls:
            ball_data["speed"][0] /= 1.5
            ball_data["speed"][1] /= 1.5
    elif type_ == "split_ball":
        for ball_data in balls[:]:
            new_ball_speed = [ball_data["speed"][0] * -1, ball_data["speed"][1]]
            new_ball_rect = ball_data["rect"].copy()
            balls.append({"rect": new_ball_rect, "speed": new_ball_speed})
    power_up_timer = pygame.time.get_ticks()

# Deactivate Power-Ups
def deactivate_power_ups():
    global paddle_expanded, invincible_ball, fast_ball, ball_color
    if paddle_expanded:
        paddle.width -= 50
        paddle_expanded = False
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

# Draw Power-Ups
def draw_power_ups():
    for power_up in power_ups:
        scaled_icon = pygame.transform.scale(power_up["icon"], (POWER_UP_WIDTH, POWER_UP_HEIGHT))
        screen.blit(scaled_icon, (power_up["rect"].x, power_up["rect"].y))

# Create Bricks for Current Level
def create_bricks():
    global bricks, level
    bricks.clear()
    for row in range(ROWS + level - 1):  # Increase rows as level increases
        for col in range(BRICKS_PER_ROW):
            brick_x = col * (BRICK_WIDTH + 5) + 35
            brick_y = row * (BRICK_HEIGHT + 5) + 50
            bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

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

    running = True
    while running:
        screen.fill(BLACK)

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
            if ball_rect.colliderect(paddle):
                ball_speed[1] = -ball_speed[1]

            # Ball Collision with Bricks
            for brick in bricks[:]:
                if ball_rect.colliderect(brick):
                    if not invincible_ball:
                        ball_speed[1] = -ball_speed[1]
                    bricks.remove(brick)
                    score += 10
                    spawn_power_up(brick.x + BRICK_WIDTH // 2, brick.y + BRICK_HEIGHT // 2)
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
            pygame.draw.rect(screen, BLUE, brick)
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
            game_over_text = font.render("Game Over! Press R to Restart", True, YELLOW)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart_game()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

# Run the Game
if __name__ == "__main__":
    main()
