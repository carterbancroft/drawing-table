# Drawing Table

A hand-crafted 2D platformer engine built with PyGame.

## Important

This is a hand-coded project. **Do not suggest changes to files, offer improvements, or refactor anything unless explicitly asked.** Answer questions, explain behavior, and make edits only when directly instructed.

## Running the Game

```bash
source venv/bin/activate
python main.py
```

## Project Structure

```
main.py               # Game loop and initialization
engine/
  entity.py           # Base Entity class (position, velocity, dimensions, z_index)
  camera.py           # Viewport tracking with clamping and is_on_camera() culling
  input_handler.py    # Keyboard state: is_pressed / is_held / is_released
  level.py            # JSON level loader, computes world width/height from tile map
  renderer.py         # Tile rendering with z-index sorting and index-based culling
  debug_overlay.py    # Monospaced HUD showing player position and camera state
game/
  player.py           # Player entity: WASD/arrow movement, gravity, triple jump, collision
data/
  levels/
    level_1.json      # 60×20 tiles at 32px (1920×640 world), spawn at x=700
```

## Architecture

### Game Loop (main.py)
```
input → player.update → debug_overlay.update → camera.update
      → renderer.draw → debug_overlay.draw → pygame.display.flip
```

Delta time is in **seconds** (`clock.tick(FPS) / 1000.0`).

### Entity System
`Entity` is a base class with `x_pos`, `y_pos`, `x_vel`, `y_vel`, `width`, `height`, `z_index`. Subclasses override `update(delta, input_handler, level)` and `draw(screen, camera)`.

### Camera
Centered on the player, clamped to level bounds. Offset applied by subtracting `camera.x_pos` / `camera.y_pos` in each entity's `draw()` method. `is_on_camera(x, y, width, height)` takes **screen-space** coordinates (already offset).

### Renderer
Pre-creates tile surfaces at startup. Sorts all layers and entities by `z_index`. Culls tiles outside the viewport using index math before iterating — no per-tile `is_on_camera` call needed.

### Level Format (JSON)
```json
{
  "tile_size": 32,
  "spawn_point": { "x": 700, "y": 0 },
  "layers": [
    {
      "name": "...",
      "z_index": 0,
      "solid": false,
      "tile_map": [[0, 1, ...], ...]
    }
  ]
}
```
`0` = empty, non-zero = tile. `solid: true` layers participate in collision detection.

### Player Physics
- Move speed: 300 px/s
- Gravity: 1500 px/s²
- Jump strength: -600 px/s (up to 3 jumps)
- `self.bottom = self.y_pos + self.height` (exclusive boundary, no `-1`)
- Collision is split: horizontal first, then vertical each frame

## Discussed Next Steps
- Camera lerping
- Sprite / animation system
- Simple enemy (validates Entity abstraction)
- Scene / state management
- Audio
