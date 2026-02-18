class Camera:
    def __init__(self, x_pos, y_pos, screen, level):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.camera_width = screen.width
        self.camera_height = screen.height
        self.level_width = level.width
        self.level_height = level.height

    def update(self, player):
        new_x_pos = player.x_pos - self.camera_width / 2
        new_y_pos = player.y_pos - self.camera_height / 2

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
