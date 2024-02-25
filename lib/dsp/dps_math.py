from math import exp, pi, sin

from ulab import numpy

try:
    from typing import Literal, Callable, List, Type, Union, MutableSequence
    from ulab.numpy import ndarray

    Sample = int
    SampleList = ndarray
    KernelFn = Callable[[float], float]
    WindowFn = Callable[[float], float]

except ImportError:
    pass


PI2 = pi * 2


def sinc(x: float) -> float:
    if x == 0:
        return 1

    return sin(pi * x) / (pi * x)


def window(x: float) -> float:
    return exp(-x / 2 * x / 2)


def sinc_kernel(window: Callable[[float], float]) -> Callable[[float], float]:
    return lambda x: sinc(x) * window(x)
