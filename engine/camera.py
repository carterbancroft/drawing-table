class Camera:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def update(self, player, screen):
        self.x_pos = player.x_pos - screen.width / 2
        self.y_pos = player.y_pos - screen.height / 2
