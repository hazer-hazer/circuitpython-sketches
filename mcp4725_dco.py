import board
from digitalio import DigitalInOut, Direction
from adafruit_mcp4725 import MCP4725
import busio
import usb_midi
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

i2c = busio.I2C(board.GP10, board.GP11)
dac = MCP4725(i2c)

reset = DigitalInOut(board.GP12)
reset.direction = Direction.OUTPUT

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

usb_midi.enable()

midi_in = usb_midi.PortIn()
midi = MIDI(midi_in=midi_in, midi_out=None)

tuning = [440 * pow(2, (freq - 69) / 12) for freq in range(0, 127)]

while True:
    midi_msg = midi.receive()

    note = None
    if midi_msg is not None:
        if isinstance(midi_msg, NoteOn):
            note = midi_msg.note

        if isinstance(midi_msg, NoteOff):
            if note == midi_msg.note:
                node = None


    if note is None:
        dac.value = 0
    else:
        dac.value = 

