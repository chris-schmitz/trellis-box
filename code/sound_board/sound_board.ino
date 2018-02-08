#include <Wire.h>
#include "Adafruit_Trellis.h"
#include "pitches.h"

#define INTPIN A4
#define SPEAKER 3

#define NUMTRELLIS 1
#define numKeys (NUMTRELLIS * 16)

Adafruit_Trellis matrix0 = Adafruit_Trellis();
Adafruit_TrellisSet trellis = Adafruit_TrellisSet(&matrix0);

void setup()
{
    Serial.begin(9600);

    pinMode(INTPIN, INPUT);
    digitalWrite(INTPIN, HIGH);

    trellis.begin(0x70);

    trellisStartupDisplay();

    Serial.println("Loading Soundboard");
}

void loop()
{
    delay(30); // this delay is required. Not totally sure why, but everything breaks if you don't include it :O

    // Serial.println("Running loop");
    // digitalWrite(13, HIGH);
    // playNote(1);
    // delay(200);
    // playNote(2);
    // delay(200);
    // playNote(3);
    // digitalWrite(13, LOW);
    // delay(300);
    // trellisStartupDisplay();
    // return;

    if (trellis.readSwitches())
    {
        for (uint8_t i = 0; i < numKeys; i++)
        {
            if (trellis.justPressed(i))
            {
                Serial.print("v");
                Serial.println(i);
                trellis.setLED(i);
                playNote(i);
            }

            if (trellis.justReleased(i))
            {
                Serial.print("^");
                Serial.println(i);
                trellis.clrLED(i);
            }
        }
        trellis.writeDisplay();
    }
}

void trellisStartupDisplay()
{
    int stepDelay = 50;
    for (uint8_t i = 0; i < numKeys; i++)
    {
        Serial.print("Trellis led on: ");
        Serial.println(i);
        trellis.setLED(i);
        trellis.writeDisplay();
        delay(stepDelay);
    }
    for (uint8_t i = 0; i < numKeys; i++)
    {
        Serial.print("Trellis led off: ");
        Serial.println(i);
        trellis.clrLED(i);
        trellis.writeDisplay();
        delay(stepDelay);
    }
}

void playNote(uint8_t i)
{
    int duration = 1000 / 8;
    int note = 0;

    if (i == 0)
    {
        note = NOTE_C3;
    }
    if (i == 1)
    {
        note = NOTE_D3;
    }
    if (i == 2)
    {
        note = NOTE_E3;
    }
    if (i == 3)
    {
        note = NOTE_F3;
    }
    if (i == 4)
    {
        note = NOTE_G3;
    }
    if (i == 5)
    {
        note = NOTE_A3;
    }
    if (i == 6)
    {
        note = NOTE_B3;
    }
    if (i == 7)
    {
        note = NOTE_C4;
    }
    if (i == 8)
    {
        note = NOTE_D4;
    }
    if (i == 9)
    {
        note = NOTE_E4;
    }
    if (i == 10)
    {
        note = NOTE_F4;
    }
    if (i == 11)
    {
        note = NOTE_G4;
    }
    if (i == 12)
    {
        note = NOTE_A4;
    }
    if (i == 13)
    {
        note = NOTE_B4;
    }
    if (i == 14)
    {
        note = NOTE_C5;
    }
    if (i == 15)
    {
        note = NOTE_D5;
    }

    tone(SPEAKER, note, duration);
}