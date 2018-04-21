import board
import pulseio
import time
import busio
import digitalio
import math
from board import SCL, SDA
from adafruit_trellis import Trellis
from lib import pitches

# === Setup the trellis ===
# Create the I2C interface
i2c = busio.I2C(SCL, SDA)
trellis = Trellis(i2c)

# === Pull in the pitches ===


# def getPitches():
#     return pitches.pitches

def getListOfPitchesStartingWithOctave(oct):
    # return a list of dictionaries for pitches starting at the C for the first octive
    print(oct)
    notes = [
        pitches.maps["%i-C" % oct],
        pitches.maps["%i-D" % oct],
        pitches.maps["%i-E" % oct],
        pitches.maps["%i-F" % oct],
        pitches.maps["%i-G" % oct],
        pitches.maps["%i-A" % oct],
        pitches.maps["%i-B" % oct],
        pitches.maps["%i-C" % (oct + 1)],
        pitches.maps["%i-D" % (oct + 1)],
        pitches.maps["%i-E" % (oct + 1)],
        pitches.maps["%i-F" % (oct + 1)],
        pitches.maps["%i-G" % (oct + 1)],
        pitches.maps["%i-A" % (oct + 1)],
        pitches.maps["%i-B" % (oct + 1)],
        pitches.maps["%i-C" % (oct + 2)],
    ]
    return notes


# === Initializing the speaker ===
speaker = pulseio.PWMOut(board.D3, variable_frequency=True)

# === setting up our frequency and duty cycle ===
OFF = 0
ON = 2**15
# So I _believe_ this is how we control the amount of voltage going to the speaker
# test it out with the oscilloscope and re-read:
# https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
# ===

# pitches = getPitches()


notes = getListOfPitchesStartingWithOctave(1)
pressedButtons = set()

while True:
    time.sleep(.1)  # required

    justPressed, released = trellis.read_buttons()

    # === add buttons that are pressed ===
    for b in justPressed:
        print('pressed: ', b)
        trellis.led[b] = True
        note = notes[b]
        speaker.frequency = note
        # speaker.duty_cycle = ON
    pressedButtons.update(justPressed)

    # === remove the butons that have been released
    for b in released:
        print('released: ', b)
        trellis.led[b] = False
    pressedButtons.difference_update(released)

    for b in pressedButtons:
        print('still pressed: ', b)
        trellis.led[b] = True

    if len(pressedButtons) == 0:
        speaker.duty_cycle = OFF
