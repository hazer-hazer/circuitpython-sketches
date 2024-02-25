import pwmio
import board
import time
import digitalio
from adafruit_debouncer import Debouncer

piezo = pwmio.PWMOut(board.A0, duty_cycle=0,
                     frequency=440, variable_frequency=True)

piezo.duty_cycle = 0  # Off

button = digitalio.DigitalInOut(board.A1)
button.switch_to_input(pull=digitalio.Pull.UP)
button = Debouncer(button)

while True:
    button.update()
    if button.fell:
        piezo.frequency = 440
        piezo.duty_cycle = 65535 // 2  # On 50%
    elif button.rose:
        piezo.duty_cycle = 0  # Off
