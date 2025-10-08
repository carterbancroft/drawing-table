import json
import os

import pygame

pygame.init()

s_width = 960
s_height = 640

screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

running = True
dt = 0

level_data_path = os.path.join("data", "levels", "level_1.json")
with open(level_data_path, "r") as f:
    level_data = json.load(f)

# Physics constants (in units per SECOND now)
MOVE_SPEED = 300  # pixels per second
GRAVITY = 1500  # pixels per second squared
JUMP_STRENGTH = -600  # pixels per second
FPS = 60
MAX_JUMPS = 3
TILE_SIZE = level_data["tile_size"]
PLAYER_HEIGHT = 48
PLAYER_WIDTH = TILE_SIZE

# Player state
player_x = level_data["spawn_point"]["x"]
player_y = level_data["spawn_point"]["y"]
player_vel_x = 0.0
player_vel_y = 0.0

jump_count = 0
is_jumping = False

sorted_layers = sorted(level_data["layers"], key=lambda layer: layer["z_index"])

# Create once before game loop
cloud_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
cloud_tile.set_alpha(128)
cloud_tile.fill((255, 255, 255))

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
    player_bottom = player_y + PLAYER_HEIGHT
    player_tile_row = int(player_bottom // TILE_SIZE)
    player_tile_left_col = int(player_x // TILE_SIZE)
    player_tile_right_col = int((player_x + PLAYER_WIDTH - 1) // TILE_SIZE)

    for layer in sorted_layers:
        if not layer["solid"]:
            continue

        tile_map = layer["tile_map"]
        if (
            tile_map[player_tile_row][player_tile_left_col] != 0
            or tile_map[player_tile_row][player_tile_right_col] != 0
        ):
            if player_vel_y > 0:
                # Collision detected
                player_y = player_tile_row * TILE_SIZE - PLAYER_HEIGHT
                player_vel_y = 0
                jump_count = 0
                is_jumping = False
                player_vel_x = 0

    # Draw
    screen.fill((135, 206, 235))
    player_drawn = False

    for layer in sorted_layers:
        tile_map = layer["tile_map"]

        if not player_drawn and level_data["player_z_index"] < layer["z_index"]:
            pygame.draw.rect(
                screen,
                (255, 100, 100),
                (int(player_x), int(player_y), PLAYER_WIDTH, PLAYER_HEIGHT),
            )
            player_drawn = True

        for row in range(len(tile_map)):
            for col in range(len(tile_map[row])):
                # Air
                tile_type = tile_map[row][col]
                if tile_type == 0:
                    continue

                # Ground
                if tile_type == 1:
                    pygame.draw.rect(
                        screen,
                        (100, 100, 100),
                        (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE),
                    )

                # Cloud
                elif tile_type == 2:
                    screen.blit(cloud_tile, (col * TILE_SIZE, row * TILE_SIZE))

    pygame.display.flip()

pygame.quit()
