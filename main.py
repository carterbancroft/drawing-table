import os

import pygame

from engine import Level, Renderer
from game import Player

pygame.init()

s_width = 960
s_height = 640

screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

running = True
dt = 0

level_data_path = os.path.join("data", "levels", "level_1.json")
level = Level(level_data_path)
renderer = Renderer(screen)

FPS = 60
TILE_SIZE = level.data["tile_size"]

player = Player(level.data["spawn_point"]["x"], level.data["spawn_point"]["y"])

while running:
    # Get delta time in seconds
    dt = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False

        player.handle_event(event)

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(dt, level)

    player_bottom = player.y_pos + player.height
    player_tile_row = int(player.bottom // TILE_SIZE)
    player_tile_left_col = int(player.x_pos // TILE_SIZE)
    player_tile_right_col = int((player.x_pos + player.width - 1) // TILE_SIZE)

    for layer in level.layers:
        if not layer["solid"]:
            continue

        tile_map = layer["tile_map"]
        if (
            tile_map[player_tile_row][player_tile_left_col] != 0
            or tile_map[player_tile_row][player_tile_right_col] != 0
        ):
            if player.y_vel > 0:
                # Collision detected
                player_y = player_tile_row * TILE_SIZE - player.height
                player_vel_y = 0
                jump_count = 0
                is_jumping = False
                player_vel_x = 0

    renderer.draw(level, [player])

pygame.quit()
