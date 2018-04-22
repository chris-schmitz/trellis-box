import board
import pulseio
import time
import random
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
indiciesToMatch = []
currentComparisonIndex = 0
userPressed = None


def reset():
    print("resetting")
    indiciesToMatch[:] = []
    currentButton = None
    currentComparisonIndex = 0


def addNewNote():
    print("adding a new note")
    newIndex = random.randint(0, 15)
    indiciesToMatch.append(newIndex)

    print("New note %d" % newIndex)
    for index in indiciesToMatch:
        trellis.led[index] = True
        speaker.frequency = notes[index]
        speaker.duty_cycle = ON
        time.sleep(1)
        speaker.duty_cycle = OFF
        trellis.led[index] = False


def success():
    trellis.led[5] = True
    trellis.led[10] = True
    speaker.frequency = pitches.maps["3-C"]
    speaker.duty_cycle = ON
    time.sleep(.2)

    trellis.led.fill(False)
    trellis.led[6] = True
    trellis.led[9] = True
    speaker.frequency = pitches.maps["4-C"]
    time.sleep(.2)

    trellis.led.fill(True)
    speaker.frequency = pitches.maps["5-C"]

    time.sleep(.5)
    trellis.led.fill(False)
    speaker.duty_cycle = OFF
    time.sleep(.5)


def failure():
    trellis.led[0] = True
    trellis.led[5] = True
    trellis.led[10] = True
    trellis.led[15] = True

    trellis.led[3] = True
    trellis.led[6] = True
    trellis.led[9] = True
    trellis.led[12] = True
    speaker.frequency = pitches.maps["3-C"]
    time.sleep(.2)
    speaker.frequency = pitches.maps["2-B"]
    time.sleep(.2)
    speaker.frequency = pitches.maps["2-A"]
    time.sleep(.5)
    trellis.led.fill(False)
    speaker.duty_cycle = OFF
    time.sleep(1)


reset()
addNewNote()

# === And let's start listening for button presses
while True:
    time.sleep(.01)  # required

    justPressed, released = trellis.read_buttons()

    # === add buttons that are pressed ===
    for b in justPressed:
        userPressed = b
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
        # print('released: ', b)

    # === matching game ===
    if userPressed is not None:
        print("time to compare")
        trellis.led[userPressed] = False

        print("user pressed: %i" % b)
        print("index to match: %i" % indiciesToMatch[currentComparisonIndex])
        print("all indexes to match: ")
        print(indiciesToMatch)
        if userPressed == indiciesToMatch[currentComparisonIndex]:
            print("the user pressed the correct button!")
            currentComparisonIndex += 1

            if currentComparisonIndex >= len(indiciesToMatch):
                print("user matched all buttons!")
                success()
                addNewNote()
                currentComparisonIndex = 0

        else:
            print("the user pressed the wrong button")
            failure()
            reset()
            addNewNote()

        userPressed = None
