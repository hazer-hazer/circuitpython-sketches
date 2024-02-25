from math import floor
import board
import displayio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
import busio
import colorsys

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(board.GP14, board.GP15)
tft_cs = board.GP17
tft_dc = board.GP12

displayio.release_displays()
display_bus = FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP13)

display = ST7735R(display_bus, width=160, height=80,
                  rotation=270, colstart=25, rowstart=1)

#
splash = displayio.Group()
display.root_group = splash

W = 80
H = 80

color_count = W * H
color_bitmap = displayio.Bitmap(W, H, color_count)
color_palette = displayio.Palette(color_count)

for x in range(W):
    for y in range(H):
        r, g, b = colorsys.hls_to_rgb(x / W, y / H, 1.0)
        color_palette[W * y + x] = (int(r), int(g), int(b))

for x in range(W):
    for y in range(H):
        color_bitmap[x, y] = W * y + x

bg_sprite = displayio.TileGrid(
    color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)

while True:
    pass

# Fading backlight
# while True:
#     now = time.monotonic()
#     if now < last_time + step_time:
#         continue

#     if i > 100:
#         i = 0

#     if i < 50:
#         pwm.duty_cycle = int(i * 2 * pwm_range / steps)
#     else:
#         pwm.duty_cycle = pwm_range - int((i - 50) * 2 * pwm_range / steps)

#     # print('pwm', pwm.duty_cycle)

#     i += 1
#     last_time = now
