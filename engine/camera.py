class Camera:
    def __init__(self, player, screen, level):
        self.width = screen.width
        self.height = screen.height
        self.level_width = level.width
        self.level_height = level.height

        self.deadzone_width = self.width / 4
        self.deadzone_height = self.height / 4

        # Center the camera around the player while clamping to level edges if necessary depending on the spawn point.
        # See comment in update for what this is doing
        self.x_pos = max(
            0,
            min(
                player.x_pos - (self.width - player.width) / 2,
                self.level_width - self.width,
            ),
        )
        self.y_pos = max(
            0,
            min(
                player.y_pos - (self.height - player.height) / 2,
                self.level_height - self.height,
            ),
        )

        # Center the deadzone within the camera
        self.deadzone_x_pos = self.x_pos - self.deadzone_width / 2
        self.deadzone_y_pos = self.y_pos - self.deadzone_height / 2

    def update(self, player):
        # Check the player's positioning relative to the deadzone and update deadzone accordingly.
        ## If the player is at the left edge of the deadzone...
        if player.center_x_pos < self.deadzone_x_pos:
            self.deadzone_x_pos = player.center_x_pos
        ## Else if the player is at the right edge of the deadzone...
        elif player.center_x_pos > self.deadzone_x_pos + self.deadzone_width:
            self.deadzone_x_pos = player.center_x_pos - self.deadzone_width

        ## If the player is at the top edge of the deadzone...
        if player.center_y_pos < self.deadzone_y_pos:
            self.deadzone_y_pos = player.center_y_pos
        ## Else if the player is at the bottom edge the deadzone...
        elif player.center_y_pos > self.deadzone_y_pos + self.deadzone_height:
            self.deadzone_y_pos = player.center_y_pos - self.deadzone_height

        # Adjust the updated camera position based on the player's current position within the deadzone
        # The max bit here clamps to the left side. The furthest left we can be is 0, move the camera
        # no further than that.
        self.x_pos = max(
            0,
            # We need to take the minimum value between the farthest right the camera can go and how far
            # the camera would go were it to remain centered around the deadzone. This effectively clamps
            # to the right side and provides a value to reference for clamping to the left side.
            min(
                # I find this little piece of math so confusing so here's the explanation for my future self.
                #
                # This calculates where to position the camera so that the deadzone is centered horizontally on screen.
                #
                # Breaking it down:
                #
                # Given:
                # - self.deadzone_x_pos = where the deadzone's left edge is in world space (say, 1000)
                # - self.camera_width = screen width (say, 800px)
                # - self.deadzone_width = deadzone width (say, 200px)
                #
                # Step by step:
                # 1. (self.camera_width - self.deadzone_width) = empty space on screen not occupied by deadzone
                #   - 800 - 200 = 600px of empty space
                # 2. / 2 = split that empty space equally on left and right sides
                #   - 600 / 2 = 300px on each side
                # 3. self.deadzone_x_pos - [that margin] = move camera LEFT by that margin
                #   - Deadzone at 1000, margin 300 → camera at 1000 - 300 = 700
                #
                # Result:
                # - Camera runs from X=700 to X=1500 (800px wide)
                # - Deadzone runs from X=1000 to X=1200 (200px wide)
                # - 300px to the left, 300px to the right = centered!
                self.deadzone_x_pos - (self.width - self.deadzone_width) / 2,
                # Camera positioned on the far right side of the level
                self.level_width - self.width,
            ),
        )

        # This does the same as above for the y axis. The explanation above applies here too.
        self.y_pos = max(
            0,
            min(
                self.deadzone_y_pos - (self.height - self.deadzone_height) / 2,
                self.level_height - self.height,
            ),
        )

        # Center the deadzone. The deadzone should always be targeted at the center of the screen, even when clamped.
        # This is really only necessary for when the camera clamps
        self.deadzone_x_pos = self.x_pos + (self.width - self.deadzone_width) / 2
        self.deadzone_y_pos = self.y_pos + (self.height - self.deadzone_height) / 2

    # Helper to determine if coordinates are within the camera's view
    def is_on_camera(self, x, y, width, height):
        if x < -width:
            return False
        if x > self.width:
            return False
        if y < -height:
            return False
        if y > self.height:
            return False

        return True

    # Convert x coordinate in the full world to coordinates within the visible screen
    def to_screen_x(self, object_world_x_pos):
        return object_world_x_pos - self.x_pos

    # Convert y coordinate in the full world to coordinates within the visible screen
    def to_screen_y(self, object_world_y_pos):
        return object_world_y_pos - self.y_pos
