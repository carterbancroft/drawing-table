import pygame


class SpriteSheet:
    def __init__(self, image_path):
        self.sheet = pygame.image.load(image_path).convert_alpha()

    def get_frame(self, x, y, width, height):
        return self.sheet.subsurface((x, y, width, height))

    def get_frame_grid(self, frame_width, frame_height, row, count):
        frames = []
        for col in range(count):
            frames.append(
                self.get_frame(
                    col * frame_width,
                    row * frame_height,
                    frame_width,
                    frame_height,
                )
            )
        return frames
