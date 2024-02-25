from array import array
import board
import time
from digitalio import DigitalInOut, Pull, Direction
from audiocore import RawSample
from analogbufio import BufferedIn
from audiopwmio import PWMAudioOut
from adafruit_waveform import sine

# mic = AnalogIn(board.A0)
# Plot each 100ms
# while True:
#     print((mic.value,))
#     time.sleep(0.1)

# NOT WORKING #

led = DigitalInOut(board.LED)
led.switch_to_output(False)
speaker = PWMAudioOut(board.A3)

# Sample to wav for 1s
record_btn = DigitalInOut(board.GP18)
record_btn.switch_to_input(Pull.DOWN)
play_btn = DigitalInOut(board.GP19)
play_btn.switch_to_input(Pull.DOWN)

rate = 44100
sample_buf = array('H', [0] * 30000)

adc_buf = BufferedIn(board.A0, sample_rate=rate)

while True:
    if record_btn.value:
        # for i in range(3):
        #     led.value = True
        #     time.sleep(0.05)
        #     led.value = False
        #     time.sleep(0.05)
        time.sleep(0.1)
        led.value = True
        start_time = time.monotonic()
        print('Recording...')
        adc_buf.readinto(sample_buf)
        led.value = False
        print(f'Recording done in {time.monotonic() - start_time}s')
    elif play_btn.value and not speaker.playing:
        print('Playing...')
        speaker.play(RawSample(sample_buf))
        speaker.stop()
