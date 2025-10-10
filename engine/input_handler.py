import pygame


class InputHandler:
    def __init__(self):
        self.current_keyboard_state = pygame.key.get_pressed()
        self.prev_keyboard_state = pygame.key.get_pressed()

    def update(self):
        # Process events, update internal state
        # Track key presses vs holds vs releases
        self.prev_keyboard_state = self.current_keyboard_state
        self.current_keyboard_state = pygame.key.get_pressed()

    def is_pressed(self, key):
        # On the first frame, prev_key_states is empty {}, so use .get() to
        # safely return False if key doesn't exist.
        return self.current_keyboard_state[key] and not self.prev_keyboard_state[key]

    def is_held(self, key):
        return self.current_keyboard_state[key]

    def is_released(self, key):
        return not self.current_keyboard_state[key] and self.prev_keyboard_state[key]
