class Entity:
    def __init__(self, x_pos, y_pos, width, height, z_index):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.center_x_pos = (x_pos + width) // 2
        self.center_y_pos = (y_pos + height) // 2
        self.x_vel = 0.0
        self.y_vel = 0.0
        self.width = width
        self.height = height
        self.z_index = z_index

    def update(self, delta, input_handler, level):
        self.center_x_pos = self.x_pos + (self.width // 2)
        self.center_y_pos = self.y_pos + (self.height // 2)

    def draw(self, screen, camera):
        pass
