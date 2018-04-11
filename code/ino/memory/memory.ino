#include <Wire.h>
#include "Adafruit_Trellis.h"
#include "pitches.h"

#define INTPIN A4
#define SPEAKER 3

#define NUMTRELLIS 1
#define numKeys (NUMTRELLIS * 16)

const int uninitalizedElement = -1;

int boxIndices[10];
int userBoxIndex = 0;
int compareIndex = 0;

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

    reset();
}

void loop()
{
    delay(30); // this delay is required. Not totally sure why, but everything breaks if you don't include it :O

    if (trellis.readSwitches())
    {
        Serial.println("user pushed button");
        for (uint8_t i = 0; i < numKeys; i++)
        {
            if (trellis.justPressed(i))
            {
                Serial.print("v");
                Serial.println(i);
                trellis.setLED(i);
                playNote(i);
                userBoxIndex = i;
            }

            if (trellis.justReleased(i))
            {
                Serial.print("^");
                Serial.println(i);
                trellis.clrLED(i);
            }
        }
        trellis.writeDisplay();

        Serial.println("=====================");
        Serial.print("userBoxIndex: ");
        Serial.println(userBoxIndex);
        Serial.print("boxIndices: ");
        Serial.println(boxIndices[compareIndex]);
        Serial.print("compareIndex: ");
        Serial.println(compareIndex);

        if (userBoxIndex == boxIndices[compareIndex])
        {
            // move out to separate function
            compareIndex++;

            Serial.print('sizeof result: ');
            Serial.println(sizeOfFixedArray(boxIndices, 10));
            if (compareIndex > sizeOfFixedArray(boxIndices, 10))
            {
                handleSuccess();
            }
            else
            {
                // nothing, wait for next button press
            }
        }
        else
        {
            handleFail();
        }
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
        playNote(i);
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

void reset()
{
    Serial.println("reset function fired");
    memset(&boxIndices[0], uninitalizedElement, 10);
    // memset(&boxIndices[0], uninitalizedElement, sizeof(boxIndices));
    userBoxIndex = 0;
    compareIndex = 0;
    addNewNote();
}

int sizeOfFixedArray(int *targetArray, int arrayLength)
{
    Serial.println("size of fixed array fired");
    int blankCount = 0;
    for (int i = 0; i < arrayLength; i++)
    {
        if (targetArray[i] == uninitalizedElement)
        {
            blankCount++;
        }
    }
    // Serial.print("array length: ");
    // Serial.println(arrayLength);
    // Serial.print("blank count: ");
    Serial.println(blankCount);
    return arrayLength - blankCount;
    // std::size_t blankCount = std::count(&targetArray[0], &targetArray[arrayLength], uninitalizedElement);
    // std::size_t filledCount = arrayLength - blankCount;
    // return filledCount;
}

void addNewNote()
{
    Serial.println("add New Note function fired");
    int randomIndex = 5;
    boxIndices[compareIndex] = randomIndex;
    playBoxIndices();
}

void playBoxIndices()
{
    for (int i = 0; i < sizeof(boxIndices); i++)
    {
        // Serial.print("index: ");
        // Serial.println(i);
        // Serial.print("boxindex: ");
        // Serial.println(boxIndices[i]);

        if (boxIndices[i] != uninitalizedElement)
        {
            trellis.clrLED(i - 1);
            playNote(i);
            trellis.setLED(i);
            trellis.writeDisplay();
        }
        delay(100);
    }
    clearAllLeds();
}

void handleSuccess()
{
    Serial.println("fire success light pattern");
    Serial.println("play success tone");

    addNewNote();
    compareIndex = 0;
}

void handleFail()
{
    Serial.println("play fail tone");
    Serial.println("fire fail light pattern");
    reset();
}

void clearAllLeds()
{
    Serial.println("clearing all LEDs");
    for (uint8_t i = 0; i < numKeys; i++)
    {
        trellis.clrLED(i);
    }

    trellis.writeDisplay();
}