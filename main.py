import os

import pygame

from engine import DebugOverlay, InputHandler, Level, Renderer
from game import Player

pygame.init()
pygame.font.init()

s_width = 960
s_height = 640

screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

level_data_path = os.path.join("data", "levels", "level_1.json")
level = Level(level_data_path)
renderer = Renderer(screen, level.data["tile_size"])
input_handler = InputHandler()
player = Player(level.data["spawn_point"]["x"], level.data["spawn_point"]["y"])
debug_overlay = DebugOverlay(25, 25)

FPS = 60
delta = 0
running = True

while running:
    # Get delta time in seconds
    delta = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False

    input_handler.update()
    player.update(delta, input_handler, level)
    debug_overlay.update(player)

    renderer.draw(level, [player])
    debug_overlay.draw(screen)

    pygame.display.flip()

pygame.quit()
