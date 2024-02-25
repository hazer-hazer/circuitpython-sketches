import array
from math import floor
import time
import busio
import board
from adafruit_ssd1306 import SSD1306_I2C
from audiocore import RawSample
from audiopwmio import PWMAudioOut
from audiocore import WaveFile
from vector import remap
from sound.wav_sample import WavSample

WIDTH = 128
HEIGHT = 32

i2c = busio.I2C(board.GP13, board.GP12)

display = SSD1306_I2C(width=WIDTH, height=HEIGHT, i2c=i2c)

wav_filepath = 'assets/sine.wav'
wav_decoder = WavSample(wav_filepath)

print(wav_decoder.show_header())

display.fill(1)
display.show()

display.fill(0)

display_wave = array.array('H', [0] * WIDTH)
for x in range(WIDTH):
    display_wave[x] = wav_decoder.lerp_box_read(
        floor(wav_decoder.length / WIDTH), (0, HEIGHT), 'rms')

# display_wave_min = min(display_wave)
# display_wave_max = max(display_wave)
# expanded_display_wave = list(map(lambda v: round(remap(
#     (display_wave_min, display_wave_max), (0, 32), v)), display_wave))

for x in range(WIDTH):
    display.pixel(x, display_wave[x], 1)

display.show()

wav_decoder.close()

while True:
    pass
