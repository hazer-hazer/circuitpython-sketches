from math import floor
import board
from display.fps import FPS
import displayio
from adafruit_st7735r import ST7735R
from adafruit_display_text import label
import busio
import terminalio
import time
import microcontroller

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

# Release any resources currently in use for the displays
displayio.release_displays()

# microcontroller.cpu.frequency = int(133e6)

baudrate = int(microcontroller.cpu.frequency / 2)

print(f'CPU frequency: {microcontroller.cpu.frequency:,}')

spi = busio.SPI(board.GP2, board.GP3)

while not spi.try_lock():
    pass
spi.configure(baudrate=baudrate)
spi.unlock()

tft_cs = board.GP7
tft_dc = board.GP6

displayio.release_displays()
display_bus = FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP5, baudrate=baudrate)

print(f'SPI baudrate: {spi.frequency:,}')

display = ST7735R(display_bus, width=160, height=80,
                  rotation=270, colstart=26, rowstart=1)

#
splash = displayio.Group()
display.root_group = splash

label = label.Label(terminalio.FONT, color=0x00ff00)
label.x = 40
label.y = 40
splash.append(label)

fps = FPS()

while True:
    label.text = f'{round(fps.value())} fps'

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
