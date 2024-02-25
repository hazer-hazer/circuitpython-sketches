import adafruit_mcp4725
import busio
import board
from digitalio import DigitalInOut, Direction
import time
import math
import array

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
i2c = busio.I2C(board.GP5, board.GP4)

dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)

DAC_MAX = 2 ** 12 - 1

delay = 0.1
step = 100

frequency = 220
length = 8000 // frequency
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(
        (1 + math.sin(math.pi * 2 * i / length)) * (DAC_MAX / 2))

while True:
    # for i in range(0, DAC_MAX, step):
    #     dac.raw_value = i
    #     time.sleep(delay)

    # for i in range(DAC_MAX, -1, -step):
    #     dac.raw_value = i
    #     time.sleep(delay)

    for v in sine_wave:
        dac.raw_value = v
