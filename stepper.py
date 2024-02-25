import time
import board
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

touch = DigitalInOut(board.GP21)
touch.direction = Direction.INPUT

stepper_pins = list(map(
    lambda pin: DigitalInOut(pin),
    [board.GP12, board.GP13, board.GP14, board.GP15]
))

for pin in stepper_pins:
    pin.direction = Direction.OUTPUT

step_seq = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

cur_step = 0


def step(dir, steps, delay):
    for _ in range(steps):
        global cur_step
        cur_step = (cur_step + dir) % len(step_seq)

        for pin_i in range(len(stepper_pins)):
            stepper_pins[pin_i].value = step_seq[cur_step][pin_i] == 1

        time.sleep(delay / 10 ** 3)


while True:
    led.value = touch.value

    if touch.value:
        step(1, 1, 1)
