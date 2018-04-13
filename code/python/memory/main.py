print("starting it up")
import time
import busio
import digitalio
from board import SCL, SDA
import board
from adafruit_trellis import Trellis
import math
import array

# === Setup the trellis ===
# Create the I2C interface
i2c = busio.I2C(SCL, SDA)
# Create a Trellis object for each board
trellis = Trellis(i2c)  # 0x70 when no I2C address is supplied
# ===

# === Setup the speaker ===
speaker = digitalio.DigitalInOut(board.D3)
speaker.direction = digitalio.Direction.OUTPUT

FREQUENCY = 440
SAMPLERATE = 400
# ===

# === Create a sample sin wave ===
length = SAMPLERATE
sine_wave = array.array("H", [0] * length)
for i in range(length):
    print(i)
    sine_wave[i] = int(math.sin(math.pi * 2 * i / 18) * (2 ** 15) + 2 ** 15)


pressedButtons = set()
while True:
    time.sleep(.1)  # necessary for reading buttons

    justPressed, released = trellis.read_buttons()
    sample = audioio.AudioOut(speaker, sine_wave)
    sample.frequency = SAMPLERATE

    for b in justPressed:
        print('pressed: ', b)
        trellis.led[b] = True
        sample.play()
    pressedButtons.update(justPressed)
    for b in released:
        print('released: ', b)
        trellis.led[b] = False
    pressedButtons.difference_update(released)
    for b in pressedButtons:
        print('still pressed: ', b)
        trellis.led[b] = True

    time.sleep(2)
    sample.stop

    # # Turn on every LED
    # print('Turning all LEDs on...')
    # trellis.led.fill(True)
    # time.sleep(2)

    # # Turn off every LED
    # print('Turning all LEDs off...')
    # trellis.led.fill(False)
    # time.sleep(2)
