import pygame

from engine import Entity


class Player(Entity):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos, width=32, height=48, z_index=1)

        self.move_speed = 300  # pixels per second
        self.gravity = 1500  # pixeld per second squared
        self.jump_strength = -600  # pixels `per second
        self.jump_count = 0
        self.max_jumps = 3
        self.is_jumping = False
        self.is_moving = False
        self.is_grounded = False
        self.bottom = self.y_pos + self.height

    def handle_input(self, input_handler):
        if input_handler.is_held(pygame.K_d) or input_handler.is_held(pygame.K_RIGHT):
            self.is_moving = True
            self.x_vel = self.move_speed
        elif input_handler.is_held(pygame.K_a) or input_handler.is_held(pygame.K_LEFT):
            self.is_moving = True
            self.x_vel = -self.move_speed
        else:
            self.is_moving = False

        if input_handler.is_pressed(pygame.K_SPACE):
            self.jump_count += 1
            if self.jump_count <= self.max_jumps:
                self.is_jumping = True
                self.is_grounded = False
                self.y_vel = self.jump_strength

        if not self.is_moving:
            # Add momentum decay here if jumping
            if self.is_jumping:
                self.x_vel *= 0.95
            else:
                self.x_vel = 0

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 100, 100),
            (int(self.x_pos), int(self.y_pos), self.width, self.height),
        )

    def update(self, delta, input_handler, level):
        self.handle_input(input_handler)

        self.x_pos += self.x_vel * delta
        self.detect_horizontal_collision(level)

        if not self.is_grounded:
            self.y_vel += self.gravity * delta

        self.y_pos += self.y_vel * delta
        self.bottom = self.y_pos + self.height
        self.detect_vertical_collision(level)

    def detect_horizontal_collision(self, level):
        tile_size = level.data["tile_size"]

        player_tile_row_above = int(self.y_pos // tile_size)
        player_tile_row_below = int((self.bottom) // tile_size)
        player_tile_col_left = int(self.x_pos // tile_size)
        player_tile_col_right = int((self.x_pos + self.width - 1) // tile_size)

        for layer in level.layers:
            if not layer["solid"]:
                continue

            tile_map = layer["tile_map"]

            # Check for right collision
            if self.x_vel > 0:  # moving right
                for row in range(player_tile_row_above, player_tile_row_below):
                    if tile_map[row][player_tile_col_right] != 0:
                        self.x_pos = player_tile_col_right * tile_size - self.width
                        self.x_vel = 0
                        break

            # Check for left collision
            if self.x_vel < 0:  # moving left
                for row in range(player_tile_row_above, player_tile_row_below):
                    if tile_map[row][player_tile_col_left] != 0:
                        self.x_pos = (player_tile_col_left + 1) * tile_size
                        self.x_vel = 0
                        break

    def detect_vertical_collision(self, level):
        tile_size = level.data["tile_size"]

        player_tile_row_above = int(self.y_pos // tile_size)
        player_tile_row_below = int((self.bottom) // tile_size)
        player_tile_col_left = int(self.x_pos // tile_size)
        player_tile_col_right = int((self.x_pos + self.width - 1) // tile_size)

        # Assume not grounded until we prove otherwise
        self.is_grounded = False

        for layer in level.layers:
            if not layer["solid"]:
                continue

            tile_map = layer["tile_map"]

            # Check for a bottom collision
            if (
                tile_map[player_tile_row_below][player_tile_col_left] != 0
                or tile_map[player_tile_row_below][player_tile_col_right] != 0
            ):
                self.is_grounded = True  # Set grounded if tile exists below

                # If we're falling...
                if self.y_vel > 0:
                    # Collision detected
                    self.y_pos = player_tile_row_below * tile_size - self.height
                    self.y_vel = 0
                    self.jump_count = 0
                    self.is_jumping = False

            # Check for top collision
            if (
                tile_map[player_tile_row_above][player_tile_col_left] != 0
                or tile_map[player_tile_row_above][player_tile_col_right] != 0
            ):
                # If we're moving up...
                if self.y_vel < 0:
                    # Collision detected
                    self.y_pos = (player_tile_row_above + 1) * tile_size
                    self.y_vel = 0
