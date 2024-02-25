import board
from digitalio import DigitalInOut, Direction
import busio
import usb_midi
from adafruit_midi import MIDI
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from pwmio import PWMOut

# i2c = busio.I2C(board.GP10, board.GP11)

reset = DigitalInOut(board.GP12)
reset.direction = Direction.OUTPUT

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

output = PWMOut(board.A0, duty_cycle=0, frequency=440, variable_frequency=True)
output.duty_cycle = 0

# usb_midi.enable()
print(usb_midi.ports)
midi = MIDI(midi_in=usb_midi.ports[0], in_channel=0)

tuning = [int(440 * pow(2, (freq - 69) / 12)) for freq in range(0, 127)]

while True:
    midi_msg = midi.receive()

    note = None
    if midi_msg is not None:
        led.value = True

        if isinstance(midi_msg, NoteOn):
            note = midi_msg.note

        if isinstance(midi_msg, NoteOff):
            if note == midi_msg.note:
                node = None
    else:
        led.value = False

    if note is not None:
        freq = tuning[note]
        print('Freq: ', freq)
        output.frequency = freq
        output.duty_cycle = 65535 // 2
    else:
        output.duty_cycle = 0
