import array
import math
import time
import board
import audiobusio
import audiocore
import audiomp3
import audiomixer

audio = audiobusio.I2SOut(board.GP9, board.GP10,
                          board.GP11, left_justified=False)


sample_rate = 41000
tone_volume = .1  # Increase or decrease this to adjust the volume of the tone.
frequency = 800  # Set this to the Hz of the tone you want to generate.
length = sample_rate // frequency  # One freqency period
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int((math.sin(math.pi * 2 * frequency * i / sample_rate) *
                        tone_volume + 1) * (2 ** 15 - 1))

sine_wave_sample = audiocore.RawSample(
    sine_wave, sample_rate=sample_rate, channel_count=1)

while True:
    audio.play(sine_wave_sample, loop=True)
    time.sleep(1)
    audio.stop()
    time.sleep(1)
