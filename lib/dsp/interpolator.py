from math import floor
from dsp.dps_math import sinc_kernel, window
from vector import lerp


try:
    from typing import Literal, Callable, Type, Union, Tuple
    from dsp.dps_math import KernelFn, SampleList, WindowFn

    InterpolationMode = Literal['point', 'cubic', 'linear', 'sinc']
except ImportError:
    pass


class Interpolator:
    length: int
    scale_factor: float
    tangent_factor: float
    sinc_filter_size: int
    kernel: KernelFn

    mode: InterpolationMode
    _interpolate: Callable[[int, SampleList], float]

    DEFAULT_MODE: InterpolationMode = 'cubic'

    index_round_method: Callable[[float], int] = floor
    sample_round_method: Callable[[float], int] = floor

    def __init__(self, from_len: int, to_len: int, mode: InterpolationMode, tension: Union[float, None] = None, sinc_filter_size: int = 1, sinc_window: WindowFn = window) -> None:
        self.length = from_len
        self.scale_factor = (from_len - 1) / to_len
        self.tangent_factor = 1 - \
            max(0, min(1, 0 if tension == None else tension))
        self.sinc_filter_size = sinc_filter_size
        self.kernel = sinc_kernel(sinc_window)

        if mode == 'point':
            self._interpolate = self.point
        elif mode == 'cubic':
            self._interpolate = self.cubic
        elif mode == 'linear':
            self._interpolate = self.linear
        elif mode == 'sinc':
            self._interpolate = self.sinc

    def get_tangent(self, k: int, samples: SampleList) -> float:
        return self.tangent_factor * (self.clipped_input(k + 1, samples) - self.clipped_input(k - 1, samples)) / 2

    def clipped_input(self, t: int, samples: SampleList) -> int:
        if 0 <= t < self.length:
            return samples[t]

        return 0

    """
    Get scaled rounded (interpolated) index and its linear interpolation factor.
    You can see this as an index of large array pointing to a smaller array, and backwards.
    The second floating point value is always in range 0.0-1.0 as it is the fractional
    part of the index scaled by the scale_factor, this can be viewed as the "way" from
    index value we get and the next index value. You can call it 'transition', 'state'.
    The last value is the original index scaled by scaled factor.
    """

    def scale_index(self, index: int) -> Tuple[int, float, float]:
        scaled = index * self.scale_factor
        index = self.index_round_method(scaled)
        return (index, scaled - index, scaled)

    def interpolate(self, index: int, samples: SampleList) -> int:
        return self.sample_round_method(self._interpolate(index, samples))

    # Modes #

    """
    Retain the samples pointed by the scale factor, skipping others.
    Streaming: allows linear streaming.
    """

    def point(self, index: int, samples: SampleList) -> float:
        return self.clipped_input(self.scale_index(index)[0], samples)

    """
    Apply linear interpolation on sample and the following one.
    Streaming: Needs 1-element forward lookup
    """

    def linear(self, index: int, samples: SampleList) -> float:
        index, lerp_factor, _ = self.scale_index(index)

        return lerp(self.clipped_input(index, samples), self.clipped_input(index + 1, samples), lerp_factor)

    """
    Streaming: Needs 1-element forward lookup
    """

    def cubic(self, index: int, samples: SampleList) -> float:
        index, trans, _ = self.scale_index(index)

        m = (self.get_tangent(index, samples),
             self.get_tangent(index + 1, samples))
        p = (self.clipped_input(index, samples),
             self.clipped_input(index + 1, samples))

        trans2 = trans ** 2
        trans3 = trans ** 3

        return p[0] * (2 * trans3 - 3 * trans2 + 1) \
            + m[0] * (trans3 - 2 * trans2 + trans) \
            + p[1] * (-2 * trans3 + 3 * trans2) \
            + m[1] * (trans3 - trans2)

    """
    Streaming: Needs buffer of sinc_filter_size * 2 + 1 elements: sinc_filter_size before and sinc_filter_size + 1 after
    """

    def sinc(self, index: int, samples: SampleList) -> float:
        index, _, scaled_index = self.scale_index(index)

        ref = range(index - self.sinc_filter_size + 1,
                    index + self.sinc_filter_size + 1)

        sum = 0
        for i in ref:
            sum += self.kernel(scaled_index - i) * \
                self.clipped_input(i, samples)

        return sum
