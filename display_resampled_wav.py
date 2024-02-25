from math import floor
import time
from analog.pot import Pot
import busio
import board
from adafruit_waveform import sine
from display.fps import FPS
from dsp.resampler import Resampler
from sound.super_sample import SuperSample
import displayio
from adafruit_displayio_ssd1306 import SSD1306
from adafruit_display_text.label import Label
import terminalio
from adafruit_st7735r import ST7735R
from adafruit_display_text.label import Label
import microcontroller

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire

WIDTH = 160
HEIGHT = 80

# microcontroller.cpu.frequency = int(250e6)

# i2c = busio.I2C(board.GP13, board.GP12)

# SSD1306 Is to Slow
# display = SSD1306_I2C(width=WIDTH, height=HEIGHT, i2c=i2c)

# Release any resources currently in use for the displays
displayio.release_displays()

baudrate = int(microcontroller.cpu.frequency / 2)
spi = busio.SPI(board.GP2, board.GP3)

while not spi.try_lock():
    pass
spi.configure(baudrate=baudrate)
spi.unlock()

print(f'SPI frequency: {spi.frequency}')

cs = board.GP7
dc = board.GP6

displayio.release_displays()
display_bus = FourWire(
    spi, command=dc, chip_select=cs, reset=board.GP5, baudrate=baudrate)

display = ST7735R(display_bus, width=WIDTH, height=HEIGHT,
                  rotation=270, colstart=26, rowstart=1, auto_refresh=False)

bitmap = displayio.Bitmap(display.width, display.height, 2)

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
root_group = displayio.Group()
root_group.append(tile_grid)

# ==========================#
sample_rate = int(4e5)
sine_wave = sine.sine_wave(sample_rate, 440)

print(f'Sine wave len')

resampled_rate = int(sample_rate / (len(sine_wave) / WIDTH))
resampled = Resampler().resample(
    sine_wave, from_rate=sample_rate, to_rate=resampled_rate)

print(f'Resampled length: {len(resampled)}')

print('resampled', resampled)

# sampler = SuperSample.from_array(
#     resampled, sample_rate=resampled_rate, channel_count=1, bit_depth=16)

# resample_rate = floor(sampler.length / WIDTH)
# print(f'resample rate {resample_rate}; length {sampler.length}')


fps = FPS()

label = Label(terminalio.FONT, color=0x00ff00)
label.x = 5
label.y = 5
root_group.append(label)
display.root_group = root_group


def draw_window():
    bitmap.fill(0)

    start = time.monotonic()

    for x in range(WIDTH):
        y = resampled[x]
        bitmap[x, y] = 1

    end = time.monotonic()
    print(f'SuperSample resampled in {end - start}s')

    label.text = f'{fps.avg()}'

    display.refresh()

# duration_ms = sampler.duration() * 1000
# display.text(f'{duration_ms}ms', 0, 0, 1, font_name='./fonts/font5x8.bin')

# display.show()


while True:
    draw_window()


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
