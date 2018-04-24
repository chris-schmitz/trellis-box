from MatchingGame import MatchingGame
import board
import pulseio
import time
import busio
import digitalio
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


def startup():
    chime = [
        pitches.maps['4-C'],
        pitches.maps['4-D'],
        pitches.maps['4-E'],
        pitches.maps['4-F'],
        pitches.maps['4-G'],
        pitches.maps['4-A'],
        pitches.maps['4-B'],
        pitches.maps['5-C'],
        pitches.maps['5-D'],
        pitches.maps['5-E'],
        pitches.maps['5-F'],
        pitches.maps['5-G'],
        pitches.maps['5-A'],
        pitches.maps['5-B'],
        pitches.maps['6-C'],
    ]

    pause = .04

    for index, note in enumerate(chime):
        trellis.led[index] = True
        speaker.frequency = note
        speaker.duty_cycle = ON
        time.sleep(pause)
        speaker.duty_cycle = OFF
    for index, note in enumerate(chime):
        trellis.led[index] = False
        time.sleep(pause)

    trellis.led[15] = True
    speaker.frequency = note
    speaker.duty_cycle = ON
    time.sleep(.08)
    speaker.duty_cycle = OFF
    trellis.led[15] = False
    time.sleep(1)


startup()

# === Grab a a list of notes (frequencies) we're going to associate with the trellis button indicies
notes = pitches.getOctavesForTrellis(3)

# === Matching game ===


game = MatchingGame(trellis, speaker, pitches)

game.reset()
game.addNewNote()

userPressed = None

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

    # === remove the butons that have been released ===
    for b in released:
        userPressed = b
        trellis.led[b] = False
        if len(justPressed) == 0:
            speaker.duty_cycle = OFF

    # === matching game ===
    if userPressed is not None:
        game.evaluateButtonPress(userPressed)
        userPressed = None
