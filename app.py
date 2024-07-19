import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load images
player_img = pygame.image.load('doodle-jumper.png')
player_img = pygame.transform.scale(player_img, (50, 50))
background_img = pygame.image.load('background.jpg')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
spring_img = pygame.image.load('spring.png')
spring_img = pygame.transform.scale(spring_img, (30, 30))  # Adjust size as needed

# Player properties
player_width = player_img.get_width()
player_height = player_img.get_height()
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5
jump_speed = -13
spring_jump_speed = -26  # 2x faster jump for spring
gravity = 0.4

# Platform properties
platform_width = 80
platform_height = 15
platform_count = 5
max_jump_height = 180

# Function to generate platforms
def generate_platforms():
    platforms = []
    for i in range(platform_count):
        if i == 0:
            platform_x = player_x
            platform_y = player_y + player_height
        else:
            platform_x = random.randint(0, WIDTH - platform_width)
            platform_y = platforms[-1]['rect'].y - random.randint(80, max_jump_height)
        
        has_spring = random.random() < 0.2  # 20% chance for a platform to have a spring
        platforms.append({
            'rect': pygame.Rect(platform_x, platform_y, platform_width, platform_height),
            'has_spring': has_spring
        })
    return platforms

# Function to draw a button
def draw_button(text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)
    return False

platforms = generate_platforms()

# Game variables
score = 0
high_score = 0
velocity_y = jump_speed
game_over = False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Apply gravity
        velocity_y += gravity
        player_y += velocity_y

        # Check for collision with platforms
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for platform in platforms:
            if player_rect.colliderect(platform['rect']) and velocity_y > 0:
                player_y = platform['rect'].top - player_height
                if platform['has_spring']:
                    velocity_y = spring_jump_speed
                else:
                    velocity_y = jump_speed

        # Move platforms down and create new ones
        if player_y < HEIGHT // 2:
            offset = HEIGHT // 2 - player_y
            player_y += offset
            for platform in platforms:
                platform['rect'].y += offset
                if platform['rect'].top > HEIGHT:
                    platforms.remove(platform)
                    new_platform_x = random.randint(0, WIDTH - platform_width)
                    new_platform_y = platforms[0]['rect'].y - random.randint(80, max_jump_height)
                    has_spring = random.random() < 0.2
                    platforms.insert(0, {
                        'rect': pygame.Rect(new_platform_x, new_platform_y, platform_width, platform_height),
                        'has_spring': has_spring
                    })
                    score += 1

        # Wrap player around screen edges
        if player_x < -player_width:
            player_x = WIDTH
        elif player_x > WIDTH:
            player_x = -player_width

        # Game over condition
        if player_y > HEIGHT:
            game_over = True
            if score > high_score:
                high_score = score

    # Draw everything
    screen.blit(background_img, (0, 0))
    if not game_over:
        screen.blit(player_img, (player_x, player_y))
        for platform in platforms:
            pygame.draw.rect(screen, BLACK, platform['rect'])
            if platform['has_spring']:
                spring_x = platform['rect'].x + platform['rect'].width // 2 - spring_img.get_width() // 2
                spring_y = platform['rect'].y - spring_img.get_height()
                screen.blit(spring_img, (spring_x, spring_y))

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
    else:
        # Game Over screen
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 48)
        
        game_over_text = font_large.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        score_text = font_medium.render(f"Your Score: {score}", True, BLUE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))

        high_score_text = font_medium.render(f"High Score: {high_score}", True, GREEN)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 10))

        if draw_button("Try Again", WIDTH // 2 - 70, HEIGHT * 3 // 4, 140, 50, YELLOW, (255, 200, 0)):
            # Reset the game
            player_x = WIDTH // 2 - player_width // 2
            player_y = HEIGHT - player_height - 10
            velocity_y = jump_speed
            score = 0
            platforms = generate_platforms()
            game_over = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()