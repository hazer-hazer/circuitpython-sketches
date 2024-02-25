import time
import board
from analogio import AnalogIn

UPDATE_THRESHOLD = 0.01

pot = AnalogIn(board.A0)
last_value = -1
value_update_threshold = 2 ** 16 * UPDATE_THRESHOLD

while True:
    if abs(last_value - pot.value) > value_update_threshold:
        print((pot.value,))
        last_value = pot.value
        time.sleep(0.01)
