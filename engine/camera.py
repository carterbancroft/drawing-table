import pygame


class Camera:
    def __init__(self, player, screen, level):
        self.x_pos = player.center_x_pos - screen.width / 2
        self.y_pos = player.center_y_pos - screen.height / 2
        self.camera_width = screen.width
        self.camera_height = screen.height
        self.level_width = level.width
        self.level_height = level.height

        self.deadzone_width = self.camera_width / 4
        self.deadzone_height = self.camera_height / 4
        self.deadzone_x_pos = player.center_x_pos - self.deadzone_width / 2
        self.deadzone_y_pos = player.center_y_pos - self.deadzone_height / 2

    def update(self, player):
        if player.center_x_pos < self.deadzone_x_pos:
            self.deadzone_x_pos = player.center_x_pos
        elif player.center_x_pos > self.deadzone_x_pos + self.deadzone_width:
            self.deadzone_x_pos = player.center_x_pos - self.deadzone_width

        if player.center_y_pos < self.deadzone_y_pos:
            self.deadzone_y_pos = player.center_y_pos
        elif player.center_y_pos > self.deadzone_y_pos + self.deadzone_height:
            self.deadzone_y_pos = player.center_y_pos - self.deadzone_height

        # Adjust the updated camera position based on the player's current position
        new_x_pos = self.deadzone_x_pos - (self.camera_width - self.deadzone_width) / 2
        new_y_pos = (
            self.deadzone_y_pos - (self.camera_height - self.deadzone_height) / 2
        )

        # print(f"new_x_pos: {new_x_pos}, new_y_pos: {new_y_pos}")

        # Lock the camera on the X axis it...
        # 1. We're at the far left of the level
        if new_x_pos < 0:
            self.x_pos = 0
        # 2. We're at the far right of the level
        elif new_x_pos > self.level_width - self.camera_width:
            self.x_pos = self.level_width - self.camera_width
        # 3. We're not on either side of the level, track the player
        else:
            self.x_pos = new_x_pos

        # Lock the camera on the Y axis if....
        # 1. We're at the top.
        if new_y_pos < 0:
            self.y_pos = 0
        # 2. We're at the bottom.
        elif new_y_pos > self.level_height - self.camera_height:
            self.y_pos = self.level_height - self.camera_height
        # 3. Not at either, track the player.
        else:
            self.y_pos = new_y_pos

    def is_on_camera(self, x, y, width, height):
        if x < -width:
            return False
        if x > self.camera_width:
            return False
        if y < -height:
            return False
        if y > self.camera_height:
            return False

        return True

    def draw_deadzone(self, screen):
        pygame.draw.rect(
            screen,
            (255, 0, 0),  # Red outline
            (
                self.deadzone_x_pos - self.x_pos,
                self.deadzone_y_pos - self.y_pos,
                self.deadzone_width,
                self.deadzone_height,
            ),
            2,  # border thickness
        )
