import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jetpack Runner")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
char_x, char_y = 100 , HEIGHT //2
char_vel_y = 0
gravity = 0.5
fly_power = -7

# Obstacles
obstacle_speed = 4
speed_increase_interval = 5000  # Speed up every 5 seconds
last_speed_increase = pygame.time.get_ticks()
obstacle_list = []
top_obstacle = True

# Score and game state
score = 0
game_over = False

# Function to create obstacles
def create_obstacle():
    global top_obstacle
    height = random.randint(50, HEIGHT // 2)
    if top_obstacle:
        obstacle_list.append({"rect": pygame.Rect(WIDTH, 0, 30, height), "passed": False})
    else:
        obstacle_list.append({"rect": pygame.Rect(WIDTH, HEIGHT - height, 30, height), "passed": False})
    top_obstacle = not top_obstacle

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Change background to white

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            char_vel_y = fly_power

    # Apply gravity
    char_vel_y += gravity
    char_y += char_vel_y
    if char_y < 0:
        char_y = 0
    elif char_y + 40 > HEIGHT:
        char_y = HEIGHT - 40

    # Create new obstacle
    if len(obstacle_list) == 0 or obstacle_list[-1]["rect"].x < WIDTH - 200:
        create_obstacle()

    # Move obstacles and check for score increment
    for obstacle in obstacle_list:
        obstacle["rect"].x -= obstacle_speed
        if not obstacle["passed"] and char_x > obstacle["rect"].x + obstacle["rect"].width:
            score += 1
            obstacle["passed"] = True

    # Remove off-screen obstacles
    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle["rect"].x > -30]

    # Collision detection
    char_rect = pygame.Rect(char_x, char_y, 40, 40)
    for obstacle in obstacle_list:
        if char_rect.colliderect(obstacle["rect"]):
            game_over = True

    # Increase game speed over time
    if pygame.time.get_ticks() - last_speed_increase > speed_increase_interval:
        obstacle_speed += 1
        last_speed_increase = pygame.time.get_ticks()

    # Draw character
    pygame.draw.rect(screen, BLACK, (char_x, char_y, 40, 40))  # Use a black rectangle for the character

    # Draw obstacles as red rectangles
    for obstacle in obstacle_list:
        pygame.draw.rect(screen, RED, obstacle["rect"])

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Game over screen
    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(over_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                char_y = HEIGHT // 2
                obstacle_list.clear()
                score = 0
                obstacle_speed = 4
                last_speed_increase = pygame.time.get_ticks()
                game_over = False
                break

    if not game_over:
        pygame.display.flip()
        clock.tick(30)

pygame.quit()