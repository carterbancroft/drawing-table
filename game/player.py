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
        self.bottom = self.y_pos + self.height

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump_count += 1
                if self.jump_count <= self.max_jumps:
                    self.is_jumping = True
                    self.y_vel = self.jump_strength

    def handle_input(self, keys):
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_vel = self.move_speed
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_vel = -self.move_speed
        else:
            # Add momentum decay here if jumping
            if self.is_jumping:
                self.vel_x *= 0.95
            else:
                self.vel_x = 0

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 100, 100),
            (int(self.x_pos), int(self.y_pos), self.width, self.height),
        )

    def update(self, delta, level):
        self.y_vel += self.gravity * delta
        self.x_pos += self.x_vel * delta
        self.y_pos += self.y_vel * delta
        self.bottom = self.y_pos + self.height
