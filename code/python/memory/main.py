import board
import pulseio
import time
import busio
import digitalio
import math
from board import SCL, SDA
from adafruit_trellis import Trellis
import pitches

# === Setup the trellis ===
# Create the I2C interface
i2c = busio.I2C(SCL, SDA)
trellis = Trellis(i2c)

# === Initializing the speaker ===
speaker = pulseio.PWMOut(board.D3, variable_frequency=True)

# === setting up our frequency and duty cycle ===
OFF = 0
ON = 2**15
# So I _believe_ this is how we control the amount of voltage going to the speaker
# test it out with the oscilloscope and re-read:
# https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
# ===


# === Grab a a list of notes (frequencies) we're going to associate with the trellis button indicies
notes = pitches.getOctavesForTrellis(3)

# === And let's start listening for button presses
while True:
    time.sleep(.01)  # required

    justPressed, released = trellis.read_buttons()

    # === add buttons that are pressed ===
    for b in justPressed:
        trellis.led[b] = True

        note = notes[b]
        speaker.frequency = note
        speaker.duty_cycle = ON

        print("===")
        print('pressed: ', b)
        print("playing note: ", note)
        print("===")

    # === remove the butons that have been released ===
    for b in released:
        trellis.led[b] = False
        if len(justPressed) == 0:
            speaker.duty_cycle = OFF

        print('released: ', b)
