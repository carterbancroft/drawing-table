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

    def draw(self, level, entities):
        self.screen.fill((135, 206, 235))
        TILE_SIZE = level.data["tile_size"]

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
                tile_map = drawable["object"]["tile_map"]
                for row in range(len(tile_map)):
                    for col in range(len(tile_map[row])):
                        tile_type = tile_map[row][col]
                        if tile_type not in self.tile_surfaces:
                            continue

                        self.screen.blit(
                            self.tile_surfaces[tile_type],
                            (col * TILE_SIZE, row * TILE_SIZE),
                        )

            if drawable["type"] == "entity":
                drawable["object"].draw(self.screen)

        pygame.display.flip()
