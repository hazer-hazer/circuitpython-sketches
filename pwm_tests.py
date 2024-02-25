from pwmio import PWMOut
import board

pwm1 = PWMOut(board.GP10, duty_cycle=50, frequency=440, variable_frequency=True)
pwm1 = PWMOut(board.GP10, duty_cycle=50, frequency=440, variable_frequency=True)
