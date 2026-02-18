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

    def draw(self, level, camera, entities):
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
                self._draw_layer(drawable["object"], camera)

            if drawable["type"] == "entity":
                drawable["object"].draw(self.screen, camera)

    def _draw_layer(self, layer, camera):
        tile_map = layer["tile_map"]

        first_col = max(0, int(camera.x_pos // self.tile_size))
        last_col = min(
            int((camera.x_pos + self.screen.width + self.tile_size) // self.tile_size),
            len(tile_map[0]),
        )

        first_row = max(0, int(camera.y_pos // self.tile_size))
        last_row = min(
            int((camera.y_pos + self.screen.height + self.tile_size) // self.tile_size),
            len(tile_map),
        )

        for row in range(first_row, last_row):
            for col in range(first_col, last_col):
                tile_type = tile_map[row][col]
                if tile_type not in self.tile_surfaces:
                    continue

                tile_x_pos = col * self.tile_size - camera.x_pos
                tile_y_pos = row * self.tile_size - camera.y_pos

                self.screen.blit(
                    self.tile_surfaces[tile_type],
                    (
                        tile_x_pos,
                        tile_y_pos,
                    ),
                )
