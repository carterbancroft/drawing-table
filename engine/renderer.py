import pygame


class Renderer:
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size
        self.tile_surfaces = {
            1: self._init_ground_tile(),
            2: self._init_cloud_tile(),
        }

    def _init_cloud_tile(self):
        surface = pygame.Surface((self.tile_size, self.tile_size))
        surface.set_alpha(128)
        surface.fill((255, 255, 255))

        return surface

    def _init_ground_tile(self):
        surface = pygame.Surface((self.tile_size, self.tile_size))
        surface.fill((100, 100, 100))

        return surface

    def draw(self, level, entities):
        self.screen.fill((135, 206, 235))

        drawables = []

        for layer in level.layers:
            drawables.append(
                {"type": "layer", "object": layer, "z_index": layer["z_index"]}
            )

        for entity in entities:
            drawables.append(
                {"type": "entity", "object": entity, "z_index": entity.z_index}
            )

        drawables.sort(key=lambda d: d["z_index"])

        for drawable in drawables:
            if drawable["type"] == "layer":
                self._draw_layer(drawable["object"])

            if drawable["type"] == "entity":
                drawable["object"].draw(self.screen)

        pygame.display.flip()

    def _draw_layer(self, layer):
        tile_map = layer["tile_map"]

        for row in range(len(tile_map)):
            for col in range(len(tile_map[row])):
                tile_type = tile_map[row][col]
                if tile_type not in self.tile_surfaces:
                    continue

                self.screen.blit(
                    self.tile_surfaces[tile_type],
                    (col * self.tile_size, row * self.tile_size),
                )
