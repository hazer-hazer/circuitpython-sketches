import time


class FPS:
    last_time: float
    avg_sum: float
    avg_cycles: int
    avg_period: float
    last_avg: float

    def __init__(self, avg_period: float = 1.0) -> None:
        self.last_time = -1
        self.avg_sum = 0.0
        self.avg_cycles = 1
        self.avg_period = avg_period
        self.last_avg = 0.0
    
    # TODO: `fix` method

    def value(self) -> float:
        now = time.monotonic()
        elapsed = now - self.last_time
        fps = 1 / (elapsed)

        self.last_time = now

        if elapsed >= self.avg_period:
            self.avg_sum = fps
            self.avg_cycles = 1
        else:
            self.avg_sum += fps
            self.avg_cycles += 1

        return fps

    def avg(self) -> float:
        self.value()
        return self.avg_sum / self.avg_cycles
