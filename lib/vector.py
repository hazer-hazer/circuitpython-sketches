try:
    from typing import Tuple
except ImportError:
    pass


def lerp(a: float, b: float, scale: float) -> float:
    return (1 - scale) * a + scale * b


def inv_lerp(a: float, b: float, value: float) -> float:
    return (value - a) / (b - a)


def remap(a_range: Tuple[int, int], b_range: Tuple[int, int], value: float) -> float:
    return lerp(b_range[0], b_range[1], inv_lerp(a_range[0], a_range[1], value))
