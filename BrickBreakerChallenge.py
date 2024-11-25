import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_RADIUS = 8
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
ROWS = 2
COLS = 10

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 36)

# High Score File
HIGH_SCORE_FILE = "highscore.txt"

# Load the highest score
def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0

# Save the highest score
def save_high_score(high_score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(high_score))

# Game variables
paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = SCREEN_HEIGHT - 50
paddle_speed = 10

ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 4
ball_dy = -4

bricks = []
for row in range(ROWS):
    for col in range(COLS):
        bricks.append(pygame.Rect(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT))

score = 0
high_score = load_high_score()  # Load high score from file
running = True

# Draw paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

# Draw ball
def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), BALL_RADIUS)

# Draw bricks
def draw_bricks():
    for brick in bricks:
        pygame.draw.rect(screen, YELLOW, brick)

# Display score and high score
def display_scores():
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

# Display end message
def display_end_screen(message):
    global high_score
    screen.fill(WHITE)
    end_text = large_font.render(message, True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(end_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))

    # Check if the current score is a new high score
    if score > high_score:
        high_score = score
        save_high_score(high_score)  # Save the new high score to the file
        high_score_message = font.render("New High Score!", True, RED)
        screen.blit(high_score_message, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    main()
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Main game loop
def main():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, bricks, score, high_score

    # Reset game variables
    paddle_x = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_dx = 4
    ball_dy = -4
    bricks = [pygame.Rect(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 50, BRICK_WIDTH, BRICK_HEIGHT) 
              for row in range(ROWS) for col in range(COLS)]
    score = 0

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with walls
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= SCREEN_WIDTH:
            ball_dx = -ball_dx
        if ball_y - BALL_RADIUS <= 0:
            ball_dy = -ball_dy

        # Ball collision with paddle
        if paddle_y < ball_y + BALL_RADIUS < paddle_y + PADDLE_HEIGHT and paddle_x < ball_x < paddle_x + PADDLE_WIDTH:
            ball_dy = -ball_dy

        # Ball collision with bricks
        for brick in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 10
                break

        # Check for game over
        if ball_y - BALL_RADIUS > SCREEN_HEIGHT:
            display_end_screen("Game Over!")

        # Check for game win
        if not bricks:
            display_end_screen("You Win!")

        # Draw everything
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks()
        display_scores()

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
