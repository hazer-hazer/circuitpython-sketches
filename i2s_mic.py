# !!!!!!!!!!!
# NOT WORKING
# !!!!!!!!!!!

import audiobusio
import board
from digitalio import DigitalInOut, Direction, Pull
import array
import audiopwmio
from audiocore import RawSample
import time
from adafruit_waveform import sine

record_btn = DigitalInOut(board.GP18)
record_btn.switch_to_input(pull=Pull.DOWN)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

mic = audiobusio.PDMIn(board.GP9, board.GP8, bit_depth=16)
audio_out = audiopwmio.PWMAudioOut(board.A0)

sample = sine.sine_wave(16e3, 440)


recording = False
while True:
    recording = record_btn.value
    led.value = recording

    if recording:
        print('Start recording...')

        mic.record(sample, len(sample))

        print('Recorded sample')
        led.value = False
    else:
        print('Playing sample...')
        audio_out.play(RawSample(sample), loop=True)
        for i in sample:
            print((i,))
        time.sleep(1)
        audio_out.stop()
