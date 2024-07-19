import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Contra-like Game")

# Colors
BLACK = (0, 0, 0)

# Player properties
player_width, player_height = 40, 60  # You may need to adjust these based on your sprite sizes
player_x, player_y = WIDTH // 4, HEIGHT - player_height - 100  # Raised the character by 100 pixels
player_speed = 5
jump_speed = -15
gravity = 0.8

player_vel_y = 0
is_jumping = False
facing_right = True
is_moving = False

# World properties
world_shift = 0
ground_height = 160  # Adjusted to match the new player position

# Load background image
background_image = pygame.image.load(os.path.join('assets', 'background.png')).convert()
background_width = background_image.get_width()
background_height = background_image.get_height()

# Scale the background image if needed
if background_height != HEIGHT:
    scale_factor = HEIGHT / background_height
    new_width = int(background_width * scale_factor)
    background_image = pygame.transform.scale(background_image, (new_width, HEIGHT))
    background_width = new_width

# Load character images
def load_images(path):
    images = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith('.png'):
            image = pygame.image.load(os.path.join(path, filename))
            images.append(image)
    return images

run_images = load_images(os.path.join('assets', 'character', 'run'))
jump_images = load_images(os.path.join('assets', 'character', 'jump'))

# Animation variables
animation_cooldown = 50  # Reduced from 100 to 50 for 2x speed
last_update = pygame.time.get_ticks()
frame = 0

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = jump_speed
                is_jumping = True
                frame = 0  # Reset frame for jump animation

    # Player movement
    keys = pygame.key.get_pressed()
    is_moving = False
    if keys[pygame.K_LEFT]:
        world_shift += player_speed
        facing_right = False
        is_moving = True
    if keys[pygame.K_RIGHT]:
        world_shift -= player_speed
        facing_right = True
        is_moving = True

    # Apply gravity
    player_vel_y += gravity
    player_y += player_vel_y

    # Check for ground collision
    if player_y > HEIGHT - player_height - ground_height:
        player_y = HEIGHT - player_height - ground_height
        player_vel_y = 0
        is_jumping = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the scrolling background
    rel_x = world_shift % background_width
    screen.blit(background_image, (rel_x - background_width, 0))
    if rel_x < WIDTH:
        screen.blit(background_image, (rel_x, 0))

    # Character animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        if is_jumping:
            frame = (frame + 1) % len(jump_images)
        elif is_moving:
            frame = (frame + 1) % len(run_images)
        last_update = current_time

    # Select the appropriate image
    if is_jumping:
        image = jump_images[frame]
    elif is_moving:
        image = run_images[frame]
    else:
        image = run_images[0]  # Use the first run image as the idle pose

    # Flip the image if facing left
    if not facing_right:
        image = pygame.transform.flip(image, True, False)

    # Draw the player
    screen.blit(image, (player_x, player_y))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)