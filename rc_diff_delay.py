from time import sleep
import board
from digitalio import DigitalInOut, Direction

output = DigitalInOut(board.GP17)
output.direction = Direction.OUTPUT
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

frequency = 440
period = 1 / frequency
duty = period / 2  #  μs
# duty *= 1e-6

timer = 0

while True:
    # now = time() * 1e-6

    # if now - timer > period:
    #     output.value = True
    #     timer = now

    output.value = True
    led.value = True
    sleep(duty)
    output.value = False
    led.value = False
    sleep(period - duty)


# Shit
