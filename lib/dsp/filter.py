# CircuitPython unsupported
# from abc import ABC, abstractmethod

try:
    from dsp.dps_math import Sample
except ImportError:
    pass


class Filter:
    def filter(self, sample: Sample) -> Sample:
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()
