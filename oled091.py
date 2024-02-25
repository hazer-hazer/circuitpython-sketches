from math import cos, pi, sin
import time
import board
import busio
import adafruit_ssd1306
from digitalio import DigitalInOut, Direction

i2c = busio.I2C(board.GP9, board.GP8)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

print('Kinda work')

last_time = 0
h_center = display.height / 2
radius = h_center - 1

while True:
    now = time.time()

    if now - last_time > 0.5:
        led.value = not led.value
        last_time = now

    display.fill(0)

    for x in range(display.width):
        angle = x * 3
        sine = int(h_center + sin(pi / 180 * angle) * radius)
        cosine = int(h_center + cos(pi / 180 * angle) * radius)

        display.pixel(x, sine, 1)
        display.pixel(x, cosine, 1)

        display.show()
