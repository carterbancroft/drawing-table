class Animator:
    def __init__(self, starting_state, frame_duration_in_seconds):
        self.current_state = starting_state
        self.current_frame = 0
        self.timer = 0
        self.frame_duration_in_seconds = frame_duration_in_seconds

    def set_state(self, state):
        self.current_state = state
        self.current_frame = 0

    def update(self, delta, possibly_updated_state):
        self.timer += delta
        if self.timer >= self.frame_duration_in_seconds:
            self.timer -= self.frame_duration_in_seconds
            self.current_frame = (self.current_frame + 1) % len(self.current_state)

        if possibly_updated_state != self.current_state:
            self.set_state(possibly_updated_state)

    def get_current_frame(self):
        return self.current_state[self.current_frame]
