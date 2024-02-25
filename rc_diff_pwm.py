# RC Differentiator
# Values used for test:
# C = 470pF
# R = 10KΩ

import time
import board
from microcontroller import Pin
from pwmio import PWMOut
from digitalio import DigitalInOut, Direction

# class RCDiff:
#     # Resistance in Ohms
#     R: int

#     # Capacitance in picofarads
#     C: int

#     pin: PWMOut

#     def __init__(self, pin: Pin, R: int, C: int) -> None:
#         self.R = R
#         self.C = C
#         self.pin = PWMOut(pin, frequency=)
#         pass

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

DUTY_MAX = 2 ** 16 - 1

pin = PWMOut(board.GP17, variable_frequency=True, frequency=5000)
delay = 5  # μs
delay *= 1e-6

assert delay * pin.frequency <= 1, \
    f"Delay must be less than PWM period; delay={delay}, Fpwm={pin.frequency}; PWM period={1 / pin.frequency}"

# pin.duty_cycle = 2 ** 15
pin.duty_cycle = int(delay / (1 / pin.frequency) * DUTY_MAX)

# fps = 60
# last_update = time.time()

led_last_update = 0

while True:
    now = time.time()
    if now - led_last_update > 0.5:
        led.value = not led.value
        led_last_update = now
    # now = time.time()
    # if now - last_update > 1 / fps:
    #     print((pin,))
    #     last_update = now

    pass
