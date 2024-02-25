from time import sleep
import board
from digitalio import DigitalInOut, Direction
import busio
from pwmio import PWMOut

# i2c = busio.I2C(board.GP10, board.GP11)

reset = DigitalInOut(board.GP16)
reset.direction = Direction.OUTPUT

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

output = PWMOut(board.GP17, duty_cycle=0, frequency=440, variable_frequency=True)
output.duty_cycle = 0

tuning = [int(440 * pow(2, (freq - 69) / 12)) for freq in range(0, 127)]

while True:
    reset.value = True
    for freq in tuning[69:79]:
        print(freq)
        output.frequency = freq
        output.duty_cycle = 65535 // 2
        sleep(0.2)
