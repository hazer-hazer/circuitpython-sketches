import board
from busio import SPI
from displayio import 

# SPI

spi = SPI(board.GP4, board.GP5, board.GP6)
spi.configure()
