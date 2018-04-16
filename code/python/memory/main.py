import board
import pulseio
import time

# Move to pitches.py
pitches = {
    "C": 261,
    "C#": 277,
    "D": 293,
    "Eb": 311,
    "E": 329,
    "F": 349,
    "F#": 370,
    "G": 392,
    "G#": 415,
    "A": 4400,
    "Bb": 466,
    "B": 493,
    # "C": 261.6,
    # "C#": 277.2,
    # "D": 293.7,
    # "Eb": 311.1,
    # "E": 329.6,
    # "F": 349.2,
    # "F#": 370.0,
    # "G": 392.0,
    # "G#": 415.3,
    # "A": 440.0,
    # "Bb": 466.2,
    # "B": 493.9,
}


# === Initializing the speaker ===
speaker = pulseio.PWMOut(board.D3, variable_frequency=True)

# === setting up our frequency and duty cycle ===
OFF = 0
ON = 2**15
# So I _believe_ this is how we control the amount of voltage going to the speaker
# test it out with the oscilloscope and re-read:
# https://learn.sparkfun.com/tutorials/pulse-width-modulation/duty-cycle
# ===

for note, frequency in pitches.items():
    print("===")
    print(note)
    print(frequency)

    speaker.frequency = frequency
    speaker.duty_cycle = ON

    time.sleep(.5)
    speaker.duty_cycle = OFF
