from time import sleep, time
from digitalio import DigitalInOut, Direction
import board

last = 0
freq = 440

period = 1 / freq
duty = 0.3
duty_period = period * duty

output = DigitalInOut(board.GP17)
output.direction = Direction.OUTPUT

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

while True:
    now = time() * 1e-9
    if now - last >= period:
        output.value = True
        last = now

    elif now - last > duty_period:
        output.value = False

    # Using sleep
    # output.value = False
    # sleep(period - duty_period)
    # output.value = True
    # sleep(duty_period)

    led.value = output.value
