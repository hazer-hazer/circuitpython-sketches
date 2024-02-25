import board
import displayio
import busio
import gc9a01

spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
display_bus = displayio.FourWire(spi, command=board.GP13, chip_select=board.GP14, reset=board.GP12)
display = gc9a01.GC9A01(display_bus, width=240, height=240, rotation=180)

bitmap = displayio.OnDiskBitmap('assets/kitty.bmp')

tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)

group = displayio.Group()
group.append(tile_grid)
display.show(group)

while True:
    pass
