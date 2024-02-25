import array
from math import floor
from random import randint
import busio
import board
from adafruit_ssd1306 import SSD1306_I2C
from adafruit_waveform import sine
from sound.super_sample import SuperSample

WIDTH = 128
HEIGHT = 64

i2c = busio.I2C(board.GP13, board.GP12)

display = SSD1306_I2C(width=WIDTH, height=HEIGHT, i2c=i2c)

sample_rate = int(4e5)
sine_wave = sine.sine_wave(sample_rate, 440)
noise = array.array('H', [0] * 128)

for i in range(len(noise)):
    noise[i] = randint(0, 2 ** 16)

sampler = SuperSample.from_array(
    sine_wave, sample_rate=sample_rate, channel_count=1, bit_depth=16)

# resample_rate = floor(sampler.length / WIDTH)
# print(f'resample rate {resample_rate}; length {sampler.length}')

display.fill(0)

for x in range(WIDTH):
    sample = sampler.lerp_box_read(
        floor(sampler.samples_count / WIDTH), (0, HEIGHT), 'rms')
    display.line(x, HEIGHT - sample // 2, x, sample // 2, 1)

display.show()

# duration_ms = sampler.duration() * 1000
# display.text(f'{duration_ms}ms', 0, 0, 1, font_name='./fonts/font5x8.bin')

# display.show()

while True:
    pass

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
