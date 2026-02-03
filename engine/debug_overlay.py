import pygame


class DebugOverlay:
    def __init__(self, x_pos, y_pos):
        self.font = pygame.font.SysFont("monospace", 25)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.surface = None

    def update(self, player):
        self.surface = self.font.render(
            f"X: {int(player.x_pos)} Y: {int(player.y_pos)}", True, (0, 0, 0)
        )

    def draw(self, screen):
        self.screen.blit(self.surface, (self.x_pos, self.y_pos))
