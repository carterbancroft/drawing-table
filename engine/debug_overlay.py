import pygame


class DebugOverlay:
    def __init__(self, x_pos, y_pos):
        self.font = pygame.font.SysFont("monospace", 18)

        self.x_pos = x_pos
        self.y_pos = y_pos

    def update(self, player, camera):
        self.player_x_debug_surface = self.font.render(
            f"Player X: {int(player.x_pos)}, {int(player.center_x_pos)}, {int(player.x_vel)}",
            True,
            (0, 0, 0),
        )

        self.player_y_debug_surface = self.font.render(
            f"Player Y: {int(player.y_pos)}, {int(player.center_y_pos)}, {int(player.y_vel)}",
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

    def draw(self, player, camera, screen):
        self.draw_text(screen)
        self.draw_deadzone(camera, screen)
        self.draw_player_center(player, camera, screen)

    def draw_text(self, screen):
        screen.blit(self.player_x_debug_surface, (self.x_pos, self.y_pos))
        screen.blit(self.player_y_debug_surface, (self.x_pos, self.y_pos + 25))
        screen.blit(self.camera_debug_surface, (self.x_pos, self.y_pos + 50))
        screen.blit(self.deadzone_debug_surface, (self.x_pos, self.y_pos + 75))

    def draw_deadzone(self, camera, screen):
        pygame.draw.rect(
            screen,
            (255, 0, 0),  # Red outline
            (
                camera.to_screen_x(camera.deadzone_x_pos),
                camera.to_screen_y(camera.deadzone_y_pos),
                camera.deadzone_width,
                camera.deadzone_height,
            ),
            3,  # border thickness
        )

    def draw_player_center(self, player, camera, screen):
        pygame.draw.line(
            screen,
            (255, 0, 0),
            (
                camera.to_screen_x(player.center_x_pos) - 10,
                camera.to_screen_y(player.center_y_pos),
            ),
            (
                camera.to_screen_x(player.center_x_pos) + 10,
                camera.to_screen_y(player.center_y_pos),
            ),
            3,
        )

        pygame.draw.line(
            screen,
            (255, 0, 0),
            (
                camera.to_screen_x(player.center_x_pos),
                camera.to_screen_y(player.center_y_pos) - 10,
            ),
            (
                camera.to_screen_x(player.center_x_pos),
                camera.to_screen_y(player.center_y_pos) + 10,
            ),
            3,
        )
