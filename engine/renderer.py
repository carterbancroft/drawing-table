import pygame


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.tile_surfaces = {
            1: self._init_ground_tile(),
            2: self._init_cloud_tile(),
        }

    def _init_cloud_tile(self):
        surface = pygame.Surface((32, 32))
        surface.set_alpha(128)
        surface.fill((255, 255, 255))

        return surface

    def _init_ground_tile(self):
        surface = pygame.Surface((32, 32))
        surface.fill((100, 100, 100))

        return surface

    def draw(self, level, player_x, player_y):
        self.screen.fill((135, 206, 235))
        player_drawn = False
        TILE_SIZE = level.data["tile_size"]
        PLAYER_WIDTH = TILE_SIZE
        PLAYER_HEIGHT = 48

        for layer in level.layers:
            tile_map = layer["tile_map"]

            if not player_drawn and level.data["player_z_index"] < layer["z_index"]:
                pygame.draw.rect(
                    self.screen,
                    (255, 100, 100),
                    (int(player_x), int(player_y), PLAYER_WIDTH, PLAYER_HEIGHT),
                )
                player_drawn = True

            for row in range(len(tile_map)):
                for col in range(len(tile_map[row])):
                    tile_type = tile_map[row][col]
                    if tile_type not in self.tile_surfaces:
                        continue

                    self.screen.blit(
                        self.tile_surfaces[tile_type],
                        (col * TILE_SIZE, row * TILE_SIZE),
                    )
        pygame.display.flip()
