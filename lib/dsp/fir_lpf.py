from math import cos, floor, pi, sin
from dsp.dps_math import PI2

from dsp.filter import Filter

try:
    from typing import List
    from dsp.dps_math import Sample
except ImportError:
    pass


class FirLpf(Filter):
    sample_rate: int
    cut_off_freq: int
    order: int

    filters: List[float]
    z_pointer: int
    z_buf: List[float]
    bit_depth: int

    def __init__(self, order: int, sample_rate: int, cut_off_freq: int, bit_depth: int) -> None:
        self.order = order
        self.sample_rate = sample_rate
        self.cut_off_freq = cut_off_freq
        self.bit_depth = bit_depth

        omega = PI2 * cut_off_freq / sample_rate
        dc = 0

        self.filters = [0.0] * (order + 1)

        for i in range(len(self.filters)):
            order_offset = i - order // 2

            if order_offset == 0:
                # This is the middle point
                self.filters[i] = omega
            else:
                self.filters[i] = sin(omega * order_offset) / order_offset
                self.filters[i] *= (0.54 - 0.46 * cos(PI2 * i / order))

            dc += self.filters[i]

        for i in range(len(self.filters)):
            self.filters[i] /= dc

        self.reset()

        # print(f'Created an FirLpf: filters: {self.filters}, sample_rate: {self.sample_rate}, cut_off_freq: {self.cut_off_freq}, order: {self.order}')

    def reset(self):
        self.init_z()

    def init_z(self):
        self.z_buf = [2 ** self.bit_depth // 2] * (len(self.filters) - 2)
        self.z_pointer = 0

    def filter(self, sample: Sample) -> Sample:
        self.z_buf[self.z_pointer] = sample

        z_buf_len = len(self.z_buf)
        out = 0
        for i in range(z_buf_len):
            out += self.filters[i] * \
                self.z_buf[(self.z_pointer + i) % z_buf_len]

        self.z_pointer = (self.z_pointer + 1) % z_buf_len

        return floor(out)

    def __str__(self) -> str:
        return f"""FirLpf ({self.order}-order) sample_rate: {self.sample_rate}, cut off frequency: {self.cut_off_freq}, bit_depth: {self.bit_depth}"""
