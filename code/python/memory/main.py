import board
import pulseio
import time
from lib import pitches


def getPitches():
    return pitches.pitches


# === Initializing the speaker ===
speaker = pulseio.PWMOut(board.D3, variable_frequency=True)

# === setting up our frequency and duty cycle ===
OFF = 0
ON = 2**15
# So I _believe_ this is how we control the amount of voltage going to the speaker
# test it out with the oscilloscope and re-read:
# https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
# ===

scale = [
    "3-C",
    "3-D",
    "3-E",
    "3-F",
    "3-G",
    "3-A",
    "3-B",
    "4-C"
]
pitches = getPitches()

for note in scale:

    frequency = pitches[note]
    print(note)
    print(frequency)

    speaker.frequency = frequency
    speaker.duty_cycle = ON

    time.sleep(.2)
    speaker.duty_cycle = OFF
