import time
import random

# === Hmmmmmm, I know we should send this in as a dependency, but I can't
# decide if they should be part of a speaker object or separate parameters or
# props we set via setters. For now I'm going to dupliacte it and finish
# moving stuff around.
OFF = 0
ON = 2**15


class MatchingGame:
    def __init__(self, trellis, speaker, pitches):
        self.trellis = trellis
        self.speaker = speaker
        self.pitches = pitches
        self.notes = []

        self.indiciesToMatch = []
        self.currentComparisonIndex = 0
        self.currentButton = None

        self._getNotes()

    def reset(self):
        print("resetting")
        self.indiciesToMatch[:] = []
        self.currentButton = None
        self.currentComparisonIndex = 0

    def addNewNote(self):
        print("adding a new note")
        newIndex = random.randint(0, 15)
        self.indiciesToMatch.append(newIndex)

        print("New note %d" % newIndex)
        for index in self.indiciesToMatch:
            self.trellis.led[index] = True
            self.speaker.frequency = self.notes[index]
            self.speaker.duty_cycle = ON
            time.sleep(1)
            self.speaker.duty_cycle = OFF
            self.trellis.led[index] = False

    def success(self):
        self.trellis.led[5] = True
        self.trellis.led[10] = True
        self.speaker.frequency = self.pitches.maps["3-C"]
        self.speaker.duty_cycle = ON
        time.sleep(.2)

        self.trellis.led.fill(False)
        self.trellis.led[6] = True
        self.trellis.led[9] = True
        self.speaker.frequency = self.pitches.maps["4-C"]
        time.sleep(.2)

        self.trellis.led.fill(True)
        self.speaker.frequency = self.pitches.maps["5-C"]

        time.sleep(.5)
        self.trellis.led.fill(False)
        self.speaker.duty_cycle = OFF
        time.sleep(.5)

    def failure(self):
        self.trellis.led[0] = True
        self.trellis.led[5] = True
        self.trellis.led[10] = True
        self.trellis.led[15] = True

        self.trellis.led[3] = True
        self.trellis.led[6] = True
        self.trellis.led[9] = True
        self.trellis.led[12] = True
        self.speaker.frequency = self.pitches.maps["3-C"]
        time.sleep(.2)
        self.speaker.frequency = self.pitches.maps["2-B"]
        time.sleep(.2)
        self.speaker.frequency = self.pitches.maps["2-A"]
        time.sleep(.5)
        self.trellis.led.fill(False)
        self.speaker.duty_cycle = OFF
        time.sleep(1)

    def evaluateButtonPress(self, buttonPressed):
        print("time to compare")
        self.trellis.led[buttonPressed] = False

        if buttonPressed == self.indiciesToMatch[self.currentComparisonIndex]:
            print("the user pressed the correct button!")
            self.currentComparisonIndex += 1

            if self.currentComparisonIndex >= len(self.indiciesToMatch):
                print("user matched all buttons!")
                self.success()
                self.addNewNote()
                self.currentComparisonIndex = 0

        else:
            print("the user pressed the wrong button")
            self.failure()
            self.reset()
            self.addNewNote()

    def _getNotes(self):
        self.notes = self.pitches.getOctavesForTrellis(3)
