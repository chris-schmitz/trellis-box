maps = {
    # === Octive 0
    "0-C": 16,
    "0-C#": 17,
    "0-D": 18,
    "0-Eb": 19,
    "0-E": 20,
    "0-F": 21,
    "0-F#": 23,
    "0-G": 24,
    "0-G#": 25,
    "0-A": 27,
    "0-Bb": 29,
    "0-B": 30,

    # === Octive 1
    "1-C": 32,
    "1-C#": 34,
    "1-D": 36,
    "1-Eb": 38,
    "1-E": 41,
    "1-F": 43,
    "1-F#": 46,
    "1-G": 49,
    "1-G#": 51,
    "1-A": 55,
    "1-Bb": 58,
    "1-B": 61,

    # === Octive 2
    "2-C": 65,
    "2-C#": 69,
    "2-D": 73,
    "2-Eb": 77,
    "2-E": 82,
    "2-F": 87,
    "2-F#": 92,
    "2-G": 98,
    "2-G#": 103,
    "2-A": 110,
    "2-Bb": 116,
    "2-B": 123,

    # === Octive 3
    "3-C": 130,
    "3-C#": 138,
    "3-D": 146,
    "3-Eb": 155,
    "3-E": 164,
    "3-F": 174,
    "3-F#": 185,
    "3-G": 196,
    "3-G#": 207,
    "3-A": 220,
    "3-Bb": 233,
    "3-B": 246,

    # === Octive 4
    "4-C": 261,
    "4-C#": 277,
    "4-D": 293,
    "4-Eb": 311,
    "4-E": 329,
    "4-F": 349,
    "4-F#": 370,
    "4-G": 392,
    "4-G#": 415,
    "4-A": 440,
    "4-Bb": 466,
    "4-B": 493,

    # === Octive 5
    "5-C": 523,
    "5-C#": 554,
    "5-D": 587,
    "5-Eb": 622,
    "5-E": 659,
    "5-F": 698,
    "5-F#": 740,
    "5-G": 784,
    "5-G#": 830,
    "5-A": 880,
    "5-Bb": 932,
    "5-B": 987,

    # === Octive 6
    "6-C": 1047,
    "6-C#": 1109,
    "6-D": 1175,
    "6-Eb": 1245,
    "6-E": 1319,
    "6-F": 1397,
    "6-F#": 1480,
    "6-G": 1568,
    "6-G#": 1661,
    "6-A": 1760,
    "6-Bb": 1865,
    "6-B": 1976,

    # === Octive 7
    "7-C": 2093,
    "7-C#": 2217,
    "7-D": 2349,
    "7-Eb": 2489,
    "7-E": 2637,
    "7-F": 2794,
    "7-F#": 2960,
    "7-G": 3136,
    "7-G#": 3322,
    "7-A": 3520,
    "7-Bb": 3729,
    "7-B": 3951,

    # === Octive 8
    "8-C": 4186,
    "8-C#": 4435,
    "8-D": 4699,
    "8-Eb": 4978,
    "8-E": 5274,
    "8-F": 5588,
    "8-F#": 5920,
    "8-G": 6272,
    "8-G#": 6645,
    "8-A": 7040,
    "8-Bb": 7459,
    "8-B": 7902,
}


def getOctavesForTrellis(startingOctave):
    '''
    (int) -> list

    startOctave: an integer between 0 and 8.

    returns a list of 24 frequencies corresponding to the buttons on the trellis.
    '''

    if type(startingOctave) is not int:
        raise ValueError("startingOctave must be an integer")

    if startingOctave < 0 or startingOctave > 8:
        raise ValueError("starting Octave must be an integer between 0 and 8")

    notes = [
        maps["%i-C" % startingOctave],
        maps["%i-D" % startingOctave],
        maps["%i-E" % startingOctave],
        maps["%i-F" % startingOctave],
        maps["%i-G" % startingOctave],
        maps["%i-A" % startingOctave],
        maps["%i-B" % startingOctave],
        maps["%i-C" % (startingOctave + 1)],
        maps["%i-D" % (startingOctave + 1)],
        maps["%i-E" % (startingOctave + 1)],
        maps["%i-F" % (startingOctave + 1)],
        maps["%i-G" % (startingOctave + 1)],
        maps["%i-A" % (startingOctave + 1)],
        maps["%i-B" % (startingOctave + 1)],
        maps["%i-C" % (startingOctave + 2)],
        maps["%i-D" % (startingOctave + 2)],
    ]
    return notes
