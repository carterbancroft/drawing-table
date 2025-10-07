import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
dt = 0

# Physics constants (in units per SECOND now)
MOVE_SPEED = 300  # pixels per second
GRAVITY = 1500  # pixels per second squared
JUMP_STRENGTH = -600  # pixels per second
FPS = 60
MAX_JUMPS = 3

# Player state
player_x = 100.0  # Use floats for smooth sub-pixel movement
player_y = 400.0
player_vel_x = 0.0
player_vel_y = 0.0

jump_count = 0
is_jumping = False

while running:
    # Get delta time in seconds
    dt = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump_count += 1
                if jump_count <= MAX_JUMPS:
                    is_jumping = True
                    player_vel_y = JUMP_STRENGTH

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_vel_x = MOVE_SPEED
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_vel_x = -MOVE_SPEED

    if is_jumping and not (
        keys[pygame.K_d]
        or keys[pygame.K_RIGHT]
        or keys[pygame.K_a]
        or keys[pygame.K_LEFT]
    ):
        player_vel_x *= 0.95

    # Update physics with delta time
    player_vel_y += GRAVITY * dt
    player_x += player_vel_x * dt
    player_y += player_vel_y * dt

    # Collision (positions are still frame-based)
    if player_y > 500:
        player_y = 500
        player_vel_y = 0
        jump_count = 0
        is_jumping = False
        player_vel_x = 0

    # Draw
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (255, 100, 100), (int(player_x), int(player_y), 32, 48))
    pygame.display.flip()

pygame.quit()
