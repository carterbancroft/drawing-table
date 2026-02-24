import pygame


class DebugOverlay:
    def __init__(self, x_pos, y_pos):
        self.font = pygame.font.SysFont("monospace", 17)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.player_debug_surface = None
        self.camera_debug_surface = None

    def update(self, player, camera):
        self.player_debug_surface = self.font.render(
            f"Player X: {int(player.x_pos)} Player Y: {int(player.y_pos)}",
            True,
            (0, 0, 0),
        )

        self.player_center_debug_surface = self.font.render(
            f"Player Center X: {int(player.center_x_pos)} Player Center Y: {int(player.center_y_pos)}",
            True,
            (0, 0, 0),
        )

        self.camera_debug_surface = self.font.render(
            f"Camera X: {int(camera.x_pos)} Camera Y: {int(camera.y_pos)}",
            True,
            (0, 0, 0),
        )

        self.deadzone_debug_surface = self.font.render(
            f"Deadzone X: {int(camera.deadzone_x_pos)} Deadzone Y: {int(camera.deadzone_y_pos)}",
            True,
            (0, 0, 0),
        )

    def draw(self, screen):
        screen.blit(self.player_debug_surface, (self.x_pos, self.y_pos))
        screen.blit(self.player_center_debug_surface, (self.x_pos, self.y_pos + 25))
        screen.blit(self.camera_debug_surface, (self.x_pos, self.y_pos + 50))
        screen.blit(self.deadzone_debug_surface, (self.x_pos, self.y_pos + 75))
