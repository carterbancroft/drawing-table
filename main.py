import os

import pygame

from engine import InputHandler, Level, Renderer
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
renderer = Renderer(screen, level.data["tile_size"])
input_handler = InputHandler()


FPS = 60

player = Player(level.data["spawn_point"]["x"], level.data["spawn_point"]["y"])

while running:
    # Get delta time in seconds
    delta = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            running = False

    input_handler.update()
    player.update(delta, input_handler, level)

    renderer.draw(level, [player])

pygame.quit()
