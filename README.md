# Earth Simulator

A small Pygame project that renders a rotating Earth against a twinkling star
field.

The simulation uses a flat world map image as a texture, scrolls that texture
horizontally, and clips the result with a circular alpha mask so the visible
area looks like a planet.

## Project Structure

```text
earth_simulator/
+-- main.py                 # Application entry point and render loop
+-- requirements.txt        # Python dependencies
+-- classes/
|   +-- earth.py            # Earth texture loading, rotation, and circular mask
|   +-- stars.py            # Random star generation and drawing
+-- config/
|   +-- screen.py           # Pygame window setup
|   +-- colors.py           # Small color lookup helper
+-- imgs/
    +-- mapa_mundi.jpg      # Main world map texture
    +-- mapa_mundi.avif     # Extra map asset, currently unused by the code
```

## Requirements

- Python 3
- Pygame 2.6.1

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the simulator:

```bash
python main.py
```

## Runtime Flow

`main.py` performs the full simulation loop:

1. Creates a Pygame screen with `screen_config()`.
2. Creates a `Stars` object with 200 stars.
3. Creates an `Earth` object with:
   - rotation speed: `0.5`
   - radius: `150`
   - screen size / center reference: `(1080, 920)`
4. Enters the main loop.
5. Handles the close-window event.
6. Clears the screen to black.
7. Draws the star field.
8. Builds the current Earth frame.
9. Draws the Earth surface centered in the window.
10. Waits 1 millisecond and flips the display buffer.

The simulation ends when the user closes the Pygame window.

## Screen Configuration

The screen size is fixed in `config/screen.py`:

```python
screen_size = (1080, 920)
```

This means:

- `screen_width = 1080`
- `screen_height = 920`

Pygame uses a 2D coordinate system where:

- `(0, 0)` is the top-left corner.
- `x` increases to the right.
- `y` increases downward.

The Earth is drawn in `main.py` at:

```python
(1080 // 2 - 150, 920 // 2 - 150)
```

Mathematically:

```text
x = screen_width / 2 - earth_radius
y = screen_height / 2 - earth_radius
```

With the current values:

```text
x = 1080 / 2 - 150 = 390
y = 920 / 2 - 150 = 310
```

The Earth surface is `300 x 300`, so placing its top-left corner at `(390, 310)`
puts its center at:

```text
earth_center_x = 390 + 150 = 540
earth_center_y = 310 + 150 = 460
```

That matches the screen center:

```text
screen_center = (1080 / 2, 920 / 2) = (540, 460)
```

## Earth Rendering

The `Earth` class is responsible for:

- Loading the map image.
- Scaling the map texture.
- Moving the map horizontally over time.
- Drawing the moving map into a square frame.
- Applying a circular alpha mask to clip the square into a planet.

### Constructor

```python
Earth(rotation_v, radius, center)
```

Current call:

```python
earth = Earth(0.5, 150, (1080, 920))
```

Parameters:

- `rotation_v`: how many pixels the map moves per frame.
- `radius`: the radius of the visible Earth circle.
- `center`: stored on the object, but currently not used by the drawing code.

### Map Scaling

The world map is loaded from:

```python
imgs/mapa_mundi.jpg
```

Then it is scaled with:

```python
pygame.transform.scale(self.map, (self.radius * 4, self.radius * 2))
```

So the map dimensions are:

```text
map_width  = 4r
map_height = 2r
```

For `r = 150`:

```text
map_width  = 4 * 150 = 600 px
map_height = 2 * 150 = 300 px
```

The visible Earth frame is:

```text
earth_frame_width  = 2r = 300 px
earth_frame_height = 2r = 300 px
```

This means the map is twice as wide as the visible circular area. The code uses
that extra width to scroll the map horizontally and create the impression that
the planet is rotating.

### Rotation Offset

The horizontal scroll position is stored in:

```python
self.x_map
```

It starts at:

```text
x_map = 0
```

Every frame, the code updates it:

```python
self.x_map -= self.rotation_v
```

Mathematically:

```text
x_map_next = x_map_current - rotation_v
```

With `rotation_v = 0.5`, the texture shifts left by half a pixel per frame.

After `n` frames:

```text
x_map(n) = -0.5n
```

So after 100 frames:

```text
x_map(100) = -50 px
```

After 1200 frames:

```text
x_map(1200) = -600 px
```

### Rotation Loop / Wraparound

The code resets the scroll offset when it has moved past the full repeated map
width:

```python
if self.x_map <= (-self.e_width * 2):
    self.x_map = 0
```

`self.e_width` is calculated as:

```python
self.e_width = self.map.get_width() // 2
```

Since `map_width = 4r`:

```text
e_width = map_width / 2 = 2r
```

The reset threshold is:

```text
-e_width * 2 = -(2r) * 2 = -4r
```

For `r = 150`:

```text
reset_threshold = -4 * 150 = -600 px
```

That is exactly the full width of the scaled map. So the texture scrolls left
from `0` to `-600`, then jumps back to `0`.

The rotation cycle length in frames is:

```text
cycle_frames = map_width / rotation_v
```

With the current values:

```text
cycle_frames = 600 / 0.5 = 1200 frames
```

The actual time for one full loop depends on the runtime frame rate. The code
uses `pygame.time.wait(1)`, but the final frame rate also depends on rendering
cost and the operating system scheduler.

If the app ran at about 60 FPS:

```text
cycle_seconds = 1200 / 60 = 20 seconds
```

### Texture Blitting

Each Earth frame is created as a transparent surface:

```python
earth_frame = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
```

Size:

```text
earth_frame = 2r x 2r
```

The map is drawn onto this frame:

```python
earth_frame.blit(self.map, (self.x_map + 2, 0))
earth_frame.blit(self.map, (self.x_map + self.e_width + self.radius * 2, 0))
```

Because:

```text
e_width = 2r
radius * 2 = 2r
```

The second blit position simplifies to:

```text
x_map + e_width + radius * 2
= x_map + 2r + 2r
= x_map + 4r
```

Since the map width is also `4r`, the second copy starts one full map width
after the first copy. This creates a repeated texture stream:

```text
first_map_x  = x_map + 2
second_map_x = x_map + 4r
```

The purpose is to prevent an empty gap while the first map scrolls out of view.

The `+ 2` offset on the first blit slightly shifts the texture to the right. It
is a small visual adjustment, not a separate physical formula.

### Circular Alpha Mask

The Earth should appear circular, but the texture is rectangular. The code
creates a transparent mask surface:

```python
self.alpha_mask = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
pygame.draw.circle(
    self.alpha_mask,
    (255, 255, 255, 255),
    (self.radius, self.radius),
    self.radius
)
```

The circle equation behind the mask is:

```text
(x - r)^2 + (y - r)^2 <= r^2
```

Where:

- `(r, r)` is the center of the mask.
- `r` is the Earth radius.
- Pixels inside the circle are visible.
- Pixels outside the circle remain transparent.

For `r = 150`, the visible circular area is:

```text
(x - 150)^2 + (y - 150)^2 <= 150^2
```

The mask is applied with:

```python
earth_frame.blit(self.alpha_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
```

`BLEND_RGBA_MIN` keeps the minimum value of each RGBA channel between the current
Earth frame and the mask.

For alpha, that means:

```text
final_alpha = min(texture_alpha, mask_alpha)
```

Inside the circle:

```text
mask_alpha = 255
final_alpha = min(texture_alpha, 255) = texture_alpha
```

Outside the circle:

```text
mask_alpha = 0
final_alpha = min(texture_alpha, 0) = 0
```

So the rectangular texture becomes transparent outside the circular mask.

## Star Field

The `Stars` class creates stars once during initialization:

```python
stars = Stars(200, (1080, 920))
```

This means 200 stars are generated inside the screen area.

Each star stores:

```text
[x, y, shine, size, offset, pulse_velocity]
```

### Star Position

The position is random:

```python
x = rd.randint(0, screen_size[0])
y = rd.randint(0, screen_size[1])
```

Mathematically:

```text
x ~ UniformInteger(0, screen_width)
y ~ UniformInteger(0, screen_height)
```

With the current screen:

```text
x ~ UniformInteger(0, 1080)
y ~ UniformInteger(0, 920)
```

`randint` includes both endpoints, so a star can be generated exactly at `x =
1080` or `y = 920`. Those positions are at the outer edge of the drawable area.

### Star Brightness

Each star starts with a random base brightness:

```python
shine = rd.randint(150, 255)
```

The star also receives two values used to animate its brightness:

```python
offset = rd.uniform(0, 2 * math.pi)
pulse_velocity = rd.uniform(0.01, 0.1)
```

`offset` is the star's current position inside a sine wave. It starts randomly
between `0` and `2pi`, so the stars do not all pulse at the same moment.

`pulse_velocity` controls how fast that star moves through the sine wave. Since
each star receives its own random velocity, some stars twinkle slowly and others
twinkle faster.

Mathematically:

```text
shine ~ UniformInteger(150, 255)
offset ~ UniformReal(0, 2pi)
pulse_velocity ~ UniformReal(0.01, 0.1)
```

During every draw call, the code advances the sine-wave position:

```python
star[4] += star[5]
```

In math form:

```text
offset_next = offset_current + pulse_velocity
```

Then it calculates the pulse:

```python
oscilation = math.sin(star[4]) * 50
```

In math form:

```text
oscillation = sin(offset) * 50
```

The sine function always returns a value between `-1` and `1`:

```text
-1 <= sin(offset) <= 1
```

Multiplying by `50` gives the brightness pulse range:

```text
-50 <= oscillation <= 50
```

So each star's brightness moves up and down by as much as 50 RGB units around
its base `shine` value.

The current brightness is calculated with:

```python
current_shine = max(50, min(255, star[2] + oscilation))
```

In math form:

```text
current_shine = clamp(shine + sin(offset) * 50, 50, 255)
```

Where:

```text
clamp(value, 50, 255) = max(50, min(255, value))
```

The clamp keeps the final brightness inside the visible RGB range used by the
simulation:

```text
50 <= current_shine <= 255
```

Without the clamp, a bright star with `shine = 255` could pulse up to:

```text
255 + 50 = 305
```

But RGB channels cannot go above `255`, so the value is limited to `255`.

The final star color is:

```python
color = (current_shine, current_shine, current_shine)
```

Because the red, green, and blue channels are equal, every star remains
grayscale. It changes brightness, but it does not change color.

In RGB color, each channel can usually range from `0` to `255`:

```text
0   = no light in that channel
255 = maximum light in that channel
```

The perceived brightness ratio can be written as:

```text
brightness = current_shine / 255
```

Examples:

```text
current_shine = 50  -> brightness = 50 / 255  = 0.196 -> about 19.6%
current_shine = 150 -> brightness = 150 / 255 = 0.588 -> about 58.8%
current_shine = 255 -> brightness = 255 / 255 = 1.000 -> 100%
```

So the updated star effect is a sine-wave twinkle:

```text
brightness over time = base shine + smooth wave motion
```

The random `offset` spreads stars across different moments in the wave, and the
random `pulse_velocity` makes stars pulse at different speeds.

### Star Size

The radius is chosen with:

```python
size = rd.choice([1, 1, 2])
```

That creates a weighted distribution:

```text
P(size = 1) = 2/3
P(size = 2) = 1/3
```

Most stars are small, and a smaller number are larger.

### Drawing Stars

Each star is drawn as a circle:

```python
pygame.draw.circle(screen, (shine, shine, shine), (x, y), size)
```

The mathematical shape is:

```text
(px - x)^2 + (py - y)^2 <= size^2
```

Where `(x, y)` is the star center and `size` is the radius.

## Timing and Frame Updates

At the end of every loop, the code calls:

```python
pygame.time.wait(1)
pygame.display.flip()
```

`pygame.time.wait(1)` asks Pygame to pause for 1 millisecond. This is not the
same as locking the simulation to a precise frame rate. It only creates a small
delay.

The Earth rotation is frame-based, not time-based:

```text
rotation_per_frame = 0.5 px
```

So the visual rotation speed depends on how many frames are rendered per second:

```text
rotation_per_second = rotation_v * FPS
```

For example:

```text
at 60 FPS: 0.5 * 60 = 30 px/s
at 120 FPS: 0.5 * 120 = 60 px/s
```

That means the planet appears to rotate faster on systems that render more
frames per second.

## Fallback Texture

If the map image fails to load, `Earth.__init__` creates a fallback surface:

```python
self.map = pygame.Surface((self.radius * 4, self.radius * 2))
self.map.fill((30, 144, 255))
pygame.draw.rect(self.map, (34, 139, 34), (50, 50, 100, 100))
```

This fallback draws:

- a blue rectangle as water
- a green rectangle as a simple land shape

It allows the simulation to keep running even if `imgs/mapa_mundi.jpg` is
missing or unreadable.

## Important Current Details

- `config/colors.py` defines `return_colors()`, but the current code does not
  use it.
- `Earth.center` is stored but not used.
- `imgs/mapa_mundi.avif` exists but is not used.
- Star positions are static, but star brightness twinkles over time with a sine
  wave.
- The Earth effect is a 2D texture scroll clipped to a circle, not a true 3D
  sphere projection.
- The map scroll speed is frame-dependent because the code does not use
  `pygame.time.Clock().tick()` or delta time.

## Main Math Summary

| Concept | Formula | Current Value |
| --- | --- | --- |
| Screen center | `(W / 2, H / 2)` | `(540, 460)` |
| Earth diameter | `2r` | `300 px` |
| Map size | `(4r, 2r)` | `(600, 300)` |
| Earth top-left | `(W / 2 - r, H / 2 - r)` | `(390, 310)` |
| Rotation update | `x_map_next = x_map - rotation_v` | `x_map_next = x_map - 0.5` |
| Wrap threshold | `-4r` | `-600 px` |
| Cycle length | `(4r) / rotation_v` | `1200 frames` |
| Circle mask | `(x - r)^2 + (y - r)^2 <= r^2` | `(x - 150)^2 + (y - 150)^2 <= 22500` |
| Star position | `x ~ U(0, W), y ~ U(0, H)` | `x ~ U(0,1080), y ~ U(0,920)` |
| Star brightness | `current_shine = clamp(shine + sin(offset) * 50, 50, 255)` | `shine ~ U(150,255)` |
| Star pulse phase | `offset_next = offset + pulse_velocity` | `offset ~ U(0,2pi)` |
| Star pulse speed | random real velocity | `pulse_velocity ~ U(0.01,0.1)` |
| Star size | weighted random choice | `P(1)=2/3, P(2)=1/3` |

## Possible Improvements

- Use `pygame.time.Clock()` to control FPS.
- Use delta time so Earth rotation speed is consistent across computers.
- Use the stored `center` value to position Earth instead of hardcoding the
  screen dimensions in `main.py`.
- Keep screen size in one shared config value so `main.py`, `Stars`, and
  `Earth` cannot drift apart.
- Add a lighting/shadow overlay to make the Earth feel more spherical.
- Tune star twinkling by changing the sine amplitude or pulse velocity range.
- Remove unused files or connect them to the running code.
