from math import floor
from adafruit_waveform import sine
from adafruit_framebuf import FrameBuffer

try:
    from typing import Tuple, Union
except ImportError:
    pass


def draw_raw_sample(display: FrameBuffer, buf, *, box: Union[Tuple[int, int, int, int], None] = None, fill_color=255, empty_color=0):
    if box == None:
        box = (0, 0, display.width, display.height)

    display.fill_rect(box[0], box[1], box[2], box[3], empty_color)

    width_factor = len(buf) / box[2]
    height_factor = box[3] / 2 ** 16

    for x in range(box[2]):
        sample_x = floor(x * width_factor)
        value = buf[sample_x]
        height_value = floor(value * height_factor)
        display.pixel(x + box[0], height_value + box[1], fill_color)
