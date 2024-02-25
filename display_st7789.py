import board
import displayio
from adafruit_st7789 import ST7789
import terminalio
from adafruit_display_text import label
import busio
import pwmio
import time

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

pwm = pwmio.PWMOut(board.GP10, frequency=5000, duty_cycle=0)

# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(board.GP10, board.GP11)

tft_cs = board.GP17
tft_dc = board.GP14

display_bus = FourWire(spi, command=tft_dc,
                       chip_select=tft_cs, reset=board.GP13)

display = ST7789(display_bus, width=240, height=240)

# Make the display context
splash = displayio.Group()
display.root_group = splash

color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(
    color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)

text = 'KEK'
font = terminalio.FONT
color = 0x000000

text_area = label.Label(font, text=text, color=color, scale=5)
text_area.x = 40
text_area.y = 40
splash.append(text_area)

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
