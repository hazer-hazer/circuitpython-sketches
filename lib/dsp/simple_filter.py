#   http://stackoverflow.com/questions/13882038/implementing-simple-high-and-low-pass-filters-in-c

from math import pi, trunc
from dsp.dps_math import PI2
from dsp.filter import Filter

try:
    from typing import Union, Literal
    from dsp.dps_math import Sample
except ImportError:
    pass


class SimpleLpf(Filter):
    sample_rate: int
    cut_off_freq: int
    bit_depth: int
    last_val: Union[float, None]

    _rc: float
    _dt: float
    _alpha: float

    def __init__(self, sample_rate: int, cut_off_freq: int, bit_depth: int) -> None:
        self.sample_rate = sample_rate
        self.cut_off_freq = cut_off_freq
        self.bit_depth = bit_depth

        self._rc = 1.0 / (self.cut_off_freq * PI2)
        self._dt = 1.0 / self.sample_rate
        self._alpha = self._dt / (self._dt + self._rc)

        self.reset()

        print(f'rc: {self._rc}, dt: {self._dt}, alpha: {self._alpha}')

    def reset(self):
        self.last_val = None

    def filter(self, sample: Sample) -> Sample:
        if self.last_val == None:
            self.last_val = sample
        else:
            self.last_val = self.last_val + \
                (self._alpha * (sample - self.last_val))

        return trunc(self.last_val)

    # def _filter(self, sample: Sample, prev: Sample) -> Sample:
    #     raise NotImplementedError()

# class SimpleLpf(SimpleFilter):
#     _alpha: float

#     def __init__(self, sample_rate: int, cut_off_freq: int, bit_depth: int) -> None:
#         super().__init__(sample_rate, cut_off_freq, bit_depth)

#         self._alpha = self._dt / (self._rc + self._dt)

#     def _filter(self, sample: Sample, prev: Sample) -> Sample:
#         return trunc(prev + self._alpha * (sample - prev))

# class SimpleHpf(SimpleFilter):
#     _alpha: float

#     def __init__(self, sample_rate: int, cut_off_freq: int, bit_depth: int) -> None:
#         super().__init__(sample_rate, cut_off_freq, bit_depth)

#         self._alpha = self._rc / (self._rc + self._dt)

#     def _filter(self, sample: Sample, prev: Sample) -> Sample:
#         return trunc(alpha * (prev + ))
