import busio
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import time

displayio.release_displays()

i2c = busio.I2C(board.GP15, board.GP14)
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)

WIDTH = 128
HEIGHT = 32

display = adafruit_displayio_ssd1306.SSD1306(
    display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(WIDTH, HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF  # White

# Draw a label
text = "Hello World!"
text_area = label.Label(
    terminalio.FONT, text=text, color=0xFFFFFF, x=28, y=HEIGHT // 2 - 1
)
splash.append(text_area)

fps_avg_sum = 0.0
fps_avg_cycle_count = 1000
fps_avg_cycle = 0

last_time = -1

while True:
    now = time.monotonic_ns()

    if now == last_time:
        continue

    fps_avg_sum += 1e9 / (now - last_time)
    fps_avg_cycle += 1

    if fps_avg_cycle >= fps_avg_cycle_count:
        text_area.text = f'{fps_avg_sum / fps_avg_cycle_count} fps'
        fps_avg_sum = 0.0
        fps_avg_cycle = 0

    last_time = now
