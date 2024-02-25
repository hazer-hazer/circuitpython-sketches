from __future__ import annotations
from array import array
from math import floor, sqrt

from vector import remap
from audiocore import RawSample
from io import BytesIO

try:
    from typing import Literal, Union, Tuple
    from circuitpython_typing import ReadableBuffer
except ImportError:
    pass


class SuperSample:
    stream: BytesIO
    sample_rate: int
    channel_count: int
    bit_depth: int

    # Start of the data, useful to reset cursor to position of the data
    # in an audio file.
    start_point: int

    # # Length of data, in bytes.
    # # Length not always known in streams.
    # # But it is required for some operations on SuperSample, thus,
    # # if it possible, it should be provided, e.g. from audio file header
    # _data_length: Union[int, None]

    # BYTES!
    _data_length: int

    # Window in count of samples (!), from-to sample numbers to read
    _window: Union[Tuple[int, int], None]

    # Precalculated (0, 2 ^ bit_depth)
    _sample_value_range: Tuple[int, int]

    def __init__(
        self,
        stream: BytesIO,
        sample_rate: int,
        channel_count: int = 1,
        bit_depth: int = 16,
        data_length: Union[int, None] = None,
        start_point: int = 0
    ) -> None:
        self.stream = stream
        self.sample_rate = sample_rate
        self.channel_count = channel_count or 1
        self.bit_depth = bit_depth
        self._data_length = data_length or stream.seek(0, 2)
        self.start_point = start_point
        self._window = None
        self._sample_value_range = (0, 2 ** bit_depth)

        self.reset()

        if self._data_length % self.byte_depth != 0:
            raise ValueError(
                f'Invalid sample data length ({self._data_length}), not divisible by byte_depth ({self.byte_depth})')

    def reset(self):
        self.stream.seek(self.start_point)
        self._window = None

    @staticmethod
    def from_array(
        arr: array,
        sample_rate: int,
        channel_count: int = 1,
        bit_depth: int = 16,
        start_point: int = 0
    ) -> SuperSample:
        # if arr.itemsize != bit_depth // 8:
        #     raise ValueError(
        #         f'Cannot construct a sample from array of elements not equal to bit_depth')

        # if arr.typecode != 'H':
        #     raise ValueError(
        #         f'Cannot construct a sample from an array of {arr.typecode}-elements')

        return SuperSample(
            BytesIO(arr),
            sample_rate=sample_rate,
            channel_count=channel_count,
            bit_depth=bit_depth,
            start_point=start_point,
            data_length=len(arr) * (bit_depth // 8)
        )

    @property
    def data_length(self):
        return self._data_length

    @property
    def byte_depth(self) -> int:
        return self.bit_depth // 8

    @property
    def samples_count(self) -> int:
        return self.data_length // self.byte_depth

    """
    !Returns full samples count, if window is not set
    """
    @property
    def samples_in_window(self) -> int:
        if self.window == None:
            return self.samples_count

        return self.window[1] - self.window[0]

    @property
    def length(self) -> int:
        if self.window:
            return (self.window[1] - self.window[0]) * self.byte_depth

        return self._data_length

    @property
    def window(self):
        return self._window

    """
    !Important!:
    - After setting window, the cursor in stream will be set to the lowest point of the window
    - Do set new window (even the same one) until you've done everything you need with the current one
    """
    @window.setter
    def window(self, win: Union[Tuple[int, int], None]):
        if win == None:
            self.stream.seek(self.start_point)
            self._window = None
            return

        if self._data_length == None:
            raise ValueError(
                'Cannot set window for sample with unknown length as it may give empty trailing bytes')

        if win[0] < 0 or win[1] < 0:
            raise ValueError(f'Window points ({win}) must be greater than 0')

        if win[0] > win[1]:
            raise ValueError(
                f'Window low point ({win[0]}) must be lower than high point ({win[1]})')

        if win[1] > self._data_length:
            raise ValueError(
                f'Window high point ({win[1]}) must be less than sample length ({self._data_length})')

        self._window = win
        self.stream.seek(self.start_point + win[0] * self.byte_depth)

    def close(self):
        self.stream.close()

    def read(self) -> int:
        if self.data_length < self.stream.tell():
            raise IndexError(
                f'Reading out of stream size ({self.data_length}), cursor at {self.stream.tell()}')
            # warnings.warn(f'Reading out of stream size ({self.data_length}), cursor at {self.stream.tell()}')

        sample = self.stream.read(self.byte_depth)
        return int.from_bytes(sample, 'little')

    def duration(self) -> float:
        if self.length == None:
            raise ValueError(
                'Cannot duration of SuperSample of unknown length')

        return 1.0 * self.length / (self.bit_depth / 8) / self.channel_count / self.sample_rate

    """
    Lerp is for linear interpolation, this is for linear resampling and only should be used in simple cases
    such as displaying the wave, not for real audio resampling

    :param Literal['sample', 'rms', 'avg'] mode: Denote the way resampling done.
        - 'sample' peaks each sample by the ratio of `resample_rate / sample_rate`
        - 'avg' takes average value of samples in a squeezed chunk to resample
        - 'rms' like 'avg' but uses root mean square
    """

    def lerp_box_read(self, resample_rate: int, resample_value_range: Union[Tuple[int, int], None] = None, mode: Literal['sample', 'rms', 'avg'] = 'sample') -> int:
        if resample_rate < 1:
            raise ValueError(
                f'Resampling rate must be greater than 1, got {resample_rate}')

        resample_value_range = resample_value_range or self._sample_value_range

        if resample_value_range[0] > resample_value_range[1]:
            raise ValueError(
                f'Invalid resampling value range, high point is less than low point in {resample_value_range}')

        sample_value = 0

        # This can be viewed as `x`-axis resampling
        if mode == 'sample':
            sample_value = self.read()

            # For `sample` just skip samples which not resampled
            # SEEK_CUR=1, CP does not have SEEK_CUR
            self.stream.seek(resample_rate - 1, 1)
        elif mode == 'avg':
            sum = 0
            for _ in range(resample_rate):
                sum += self.read()
            sample_value = sum / resample_rate
        elif mode == 'rms':
            sq_sum = 0
            for _ in range(resample_rate):
                sq_sum += self.read() ** 2
            mean = sq_sum / resample_rate
            sample_value = sqrt(mean)
        else:
            raise TypeError(
                f'Invalid or unsupported `mode` parameter `{mode}` in `lerp_read`')

        # Return resampled value (`y`-axis resampling)
        return floor(remap(self._sample_value_range, resample_value_range, sample_value))

    def lerp_read(self, resample_rate: int, resample_bit_depth: Union[int, None], mode: Literal['sample', 'rms', 'avg'] = 'sample') -> int:
        if resample_rate < 1:
            raise ValueError('resample_rate must be greater than 1')

        resample_bit_depth = resample_bit_depth or self.bit_depth

        return self.lerp_box_read(resample_rate=resample_rate, resample_value_range=(0, 2 ** resample_bit_depth), mode=mode)
