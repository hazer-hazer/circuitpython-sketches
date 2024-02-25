import array
from io import BytesIO
from math import ceil, floor
from random import randint
import time
from analog.pot import Pot
import busio
import board
from adafruit_ssd1306 import SSD1306_I2C
from adafruit_waveform import sine
from display.fps import FPS
from sound.super_sample import SuperSample
import displayio
from adafruit_st7735r import ST7735R
from adafruit_displayio_ssd1306 import SSD1306
from sound.wav_sample import WavSample
import terminalio
from adafruit_display_text.label import Label
import microcontroller

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

WIDTH = 128
HEIGHT = 64

# microcontroller.cpu.frequency = int(250e6)

# i2c = busio.I2C(board.GP13, board.GP12)

# SSD1306 Is to Slow
# display = SSD1306_I2C(width=WIDTH, height=HEIGHT, i2c=i2c)

# Release any resources currently in use for the displays
displayio.release_displays()

baudrate = int(1e5)
spi = busio.SPI(board.GP14, board.GP15)

while not spi.try_lock():
    pass
spi.configure(baudrate=baudrate)
spi.unlock()

cs = board.GP17
dc = board.GP12

displayio.release_displays()
display_bus = FourWire(
    spi, command=dc, chip_select=cs, reset=board.GP13, baudrate=baudrate)

# display = ST7735R(display_bus, width=WIDTH, height=HEIGHT,
#                   rotation=270, colstart=26, rowstart=1, auto_refresh=False)

display = SSD1306(display_bus, width=WIDTH, height=HEIGHT, auto_refresh=False)

bitmap = displayio.Bitmap(display.width, display.height, 2)

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
root_group = displayio.Group()
root_group.append(tile_grid)
display.root_group = root_group

sample_rate = int(44100)

# Sine wave
# sine_wave = sine.sine_wave(sample_rate, 10)

# sampler = SuperSample(BytesIO(sine_wave),
#                       sample_rate=sample_rate, channel_count=1, bit_depth=16)

sampler = WavSample(open('./assets/dip.wav', 'rb'))

draw_bench = -1


def draw_window():
    assert sampler.samples_in_window

    resample_rate = floor(sampler.samples_in_window / WIDTH)
    print(f'resample to rate {resample_rate}. from {sampler.sample_rate}')

    bitmap.fill(0)

    start = time.monotonic()

    for x in range(WIDTH):
        sample = sampler.lerp_box_read(resample_rate, (0, HEIGHT), 'rms')
        bitmap[x, sample] = 1

    end = time.monotonic()
    print(f'resampled in {end - start}s')

    display.refresh()


# Show the second half of the sample
# sampler.window = (sampler.samples_count // 2, sampler.samples_count)


draw_window()

# Using pots
# I set such a threshold so the whole count of differences
# between read values is equal to the number of pixels
# we can offset by on side
l_pot = Pot(board.A0, threshold=2 / WIDTH)
r_pot = Pot(board.A1, threshold=2 / WIDTH, inverted=True)

max_trim_length = floor(sampler.samples_count / 2)


def get_window():
    print(f'Pots: {l_pot.value()}, {r_pot.value()}')
    return (floor(l_pot.real_value() * max_trim_length), floor(sampler.samples_count - r_pot.real_value() * max_trim_length))


fps = FPS()

fps_label = Label(terminalio.FONT, color=0x00ff00, anchor=(0, 0))
fps_label.x = 0
fps_label.y = 5
root_group.append(fps_label)

# TODO: Async
while True:
    fps_label.text = f'{fps.value()}fps'

    if l_pot.changed or r_pot.changed:
        win = get_window()

        if (win[1] - win[0]) / WIDTH > 1:
            print(f'Window: {win}')
            print((l_pot.real_value(), r_pot.real_value()))
            sampler.window = win
            draw_window()
        else:
            print(f'Ignore window {win}, to small')

# The compilation of this sketch as a function

# def draw_raw_sample(display: FrameBuffer, buf, *, box: Union[Tuple[int, int, int, int], None] = None, fill_color=255, empty_color=0):
#     if box == None:
#         box = (0, 0, display.width, display.height)

#     display.fill_rect(box[0], box[1], box[2], box[3], empty_color)

#     width_factor = len(buf) / box[2]
#     height_factor = box[3] / 2 ** 16

#     for x in range(box[2]):
#         sample_x = floor(x * width_factor)
#         value = buf[sample_x]
#         height_value = floor(value * height_factor)
#         display.pixel(x + box[0], height_value + box[1], fill_color)


# sample_buf = sine.sine_wave(5e5, 440)
# sample = RawSample(sample_buf)

# display.fill(1)
# draw_raw_sample(display=display, buf=sample_buf)
# display.show()

# # Just play audio
# audio_out = PWMAudioOut(board.A0)

# while True:
#     if not audio_out.playing:
#         audio_out.play(sample, loop=True)
