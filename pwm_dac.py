import time
import board
from microcontroller import Pin
from pwmio import PWMOut
from digitalio import DigitalInOut, Direction
import microcontroller

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

# RESOLUTION_FREQUENCIES = {
#     res: freq for res in range(MIN_RESOLUTION, MAX_RESOLUTION + 1)
# }

class PWMDAC():
    pin: PWMOut
    resolution: int

    # 8 Is the lowest "good"
    MIN_RESOLUTION: int = 8
    # Pico max PWM resolution
    MAX_RESOLUTION: int = 16

    def __init__(self, pin: Pin, resolution: int = 8) -> None:
        self.pin = PWMOut(pin, frequency=int(
            microcontroller.cpu.frequency / 32))
        self.resolution = resolution
        pass

    def write(self, value: float):
        self.pin.duty_cycle = int((2 ** PWMDAC.MAX_RESOLUTION - 1) * value)
        # self.pin.duty_cycle = int(100000 * value)


pwm_dac = PWMDAC(board.GP16)

while True:
    for i in range(1, 6):
        pwm_dac.write(i / 5)
        time.sleep(1)
