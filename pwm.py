import board
from pwmio import PWMOut

pwm = PWMOut(board.GP17, frequency=440, duty_cycle=2 ** 15)

while True:
    pass
