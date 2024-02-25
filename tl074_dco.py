import time
import board
from microcontroller import Pin
from pwmio import PWMOut
from digitalio import DigitalInOut, Direction
import microcontroller

TUNING = [int(440 * pow(2, (freq - 69) / 12)) for freq in range(0, 127)]


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


class Voice:
    reset_pin: PWMOut
    # range_pwm_pin: PWMDAC
    range_pwm_pin: PWMOut
    freq: float

    def __init__(self, reset_pin: Pin, range_pwm_pin: Pin) -> None:
        self.reset_pin = PWMOut(reset_pin, variable_frequency=True)
        self.range_pwm_pin = PWMOut(range_pwm_pin, variable_frequency=True)
        # self.range_pwm_pin = PWMDAC(range_pwm_pin)

    def set_note(self, note: int):
        if note is None:
            # self.range_pwm_pin.write(0)
            self.range_pwm_pin.duty_cycle = 0
            self.reset_pin.frequency = 0
            return

        self.freq = TUNING[note]
        self.reset_pin.frequency = self.freq
        self.reset_pin.duty_cycle = 0
        self.range_pwm_pin.frequency = self.freq
        self.range_pwm_pin.duty_cycle = 0


led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

voice = Voice(board.GP17, board.GP15)

while True:
    led.value = True
    voice.set_note(79)
    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)

    pass
