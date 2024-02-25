from microcontroller import Pin
from analogio import AnalogIn


class Pot:
    analog_in: AnalogIn
    last_value: int
    threshold_value: float
    inverted: bool

    def __init__(self, pin: Pin, threshold: float = 0.01, inverted: bool = False) -> None:
        self.analog_in = AnalogIn(pin)
        self.threshold_value = 2 ** 16 * threshold
        self.inverted = inverted

        self.last_value = 0
        # Read initial value
        self.value()

        if threshold < 0 or threshold > 1.0:
            raise ValueError('Pot threshold must be in range 0-1.0')

    @property
    def changed(self) -> bool:
        return abs(self.last_value - self.analog_in.value) > self.threshold_value

    def value(self) -> int:
        if self.changed:
            val = self.analog_in.value
            self.last_value = 2 ** 16 - val if self.inverted else val

        return self.last_value

    def real_value(self) -> float:
        return self.value() / 2 ** 16
