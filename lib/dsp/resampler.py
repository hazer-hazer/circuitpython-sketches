from array import array
from math import ceil

from dsp.dps_math import window
from dsp.filter import Filter
from dsp.fir_lpf import FirLpf
from dsp.interpolator import Interpolator
from dsp.simple_filter import SimpleLpf

try:
    from typing import Dict, Literal, Union
    from dsp.dps_math import SampleList, WindowFn
    from dsp.interpolator import InterpolationMode

    LpfKind = Literal['IIR', 'FIR', 'auto']
except ImportError:
    pass


class Resampler:
    DEFAULT_LPF_USE: Dict[InterpolationMode, bool] = {
        'point': False,
        'linear': False,
        'cubic': True,
        'sinc': True,
    }

    DEFAULT_LPF_ORDER: Dict[LpfKind, int] = {
        'IIR': 16,
        'FIR': 71,
    }

    DEFAULT_LPF: Dict[LpfKind, Filter]

    def __init__(self) -> None:
        pass

    def resample(
        self,
        samples: SampleList,
        from_rate: int,
        to_rate: int,
        bit_depth: int = 16,
        mode: InterpolationMode = Interpolator.DEFAULT_MODE,
        tension: float = 0,
        sinc_filter_size: int = 6,
        sinc_window: WindowFn = window,
        use_lpf: Union[LpfKind, None] = 'auto',
        lpf_order: Union[int, None] = None
    ) -> SampleList:
        rate = ((to_rate - from_rate) / from_rate) + 1
        # rate = to_rate / from_rate
        orig_len = len(samples)
        resampled_len = ceil(orig_len * rate)
        # resampled_len = len(samples) * ceil(to_rate / from_rate)
        # TODO: Dynamic bit depth
        resampled = array('H', [0] * resampled_len)

        interpolator = Interpolator(orig_len, resampled_len, mode=mode,
                                    tension=tension, sinc_filter_size=sinc_filter_size, sinc_window=sinc_window)

        lpf = None
        if use_lpf == 'IIR':
            raise ValueError('IIR Filter not supported yet')

        if use_lpf == 'auto':
            use_lpf = 'FIR'

        if use_lpf:
            lpf_order = lpf_order or Resampler.DEFAULT_LPF_ORDER[use_lpf]

            if from_rate < to_rate:
                lpf = FirLpf(lpf_order, to_rate, from_rate //
                             2, bit_depth=bit_depth)
                print(
                    f'Up-sampling from {from_rate} to {to_rate}. rate: {rate}. result length: {resampled_len}, using filter {lpf}')
                self.upsample(samples, resampled, interpolator, lpf)
            else:
                lpf = FirLpf(lpf_order, from_rate, to_rate //
                             2, bit_depth=bit_depth)
                print(
                    f'Down-sampling from {from_rate} to {to_rate}. rate: {rate}. result length: {resampled_len}, using filter {lpf}')
                self.downsample(samples, resampled, interpolator, lpf)
        else:
            print(f'Resampling without LPF using interpolation')
            self.interpolate(samples, resampled, interpolator)

        return resampled

    # @staticmethod
    # def choose_lpf(interpolation_mode: InterpolationMode) -> Filter:

    def upsample(self, samples: SampleList, result: SampleList, interpolator: Interpolator, filter: Filter):
        for i in range(len(samples)):
            result[i] = filter.filter(interpolator.interpolate(i, samples))

        filter.reset()

        for i in reversed(range(len(result))):
            filter.filter(result[i])

    def downsample(self, samples: SampleList, result: SampleList, interpolator: Interpolator, filter: Filter):
        for i in range(len(samples)):
            filter.filter(samples[i])

        filter.reset()

        for i in range(len(samples)):
            filter.filter(samples[i])

        self.interpolate(samples, result, interpolator)

    def interpolate(self, samples: SampleList, result: SampleList, interpolator: Interpolator):
        for i in range(len(result)):
            interpolator.interpolate(i, samples)


print('kek')
