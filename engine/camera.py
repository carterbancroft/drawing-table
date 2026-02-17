class Camera:
    def __init__(self, x_pos, y_pos, screen):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.screen_width = screen.width
        self.screen_height = screen.height

    def update(self, player):
        self.x_pos = player.x_pos - self.screen_width / 2
        self.y_pos = player.y_pos - self.screen_height / 2

    def is_on_camera(self, x, y, width, height):
        if x < -width:
            return False
        if x > self.screen_width:
            return False
        if y < -height:
            return False
        if y > self.screen_height:
            return False

        return True
