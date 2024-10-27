#include "SD.h"
#define SD_ChipSelectPin 10 
//PINS for sd card module
//CS = 10
//SCK = 13
//MOSI = 11
//MISO = 12
#include "TMRpcm.h"
#include "SPI.h"

TMRpcm sound;
int moisture;
int index1 = 0;
int index2 = 0;

int relayPin = 5;
//PINS
//COM = Positive powerSupply
//NO(Normally Open) = Red wire of the water pump
//Ground of the power source and black wire of the water must be connected
void setup() {
  
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  sound.speakerPin=9; //Pin 9 for Speaker
  if (!SD.begin(SD_ChipSelectPin)){
    Serial.println("SD fail");
  return;
  }
}

void loop() {
  int moisture = digitalRead(2); // Read moisture sensor value
    Serial.println(moisture);
   if (moisture == 1) { // If moisture is detected (1)
   index2 = 0;
      if (index1 == 0){
          sound.stopPlayback();// Stop the sound
          index1++;
      }
        if (!sound.isPlaying()) { // If sound is not already playing
            sound.setVolume (5);
            sound.play("abcd.wav"); // Optionally play another sound        
            }
      digitalWrite(relayPin, HIGH);
    } else if (moisture == 0) { // If moisture is low (0)
        index1 = 0;
        if (index2 == 0){
          sound.stopPlayback(); // Stop the sound
          index2++;
        }
        if (!sound.isPlaying()) { // If sound is currently playing
             sound.setVolume (5);
            sound.play("asdf.wav"); // Play the sound

        }
        
       digitalWrite(relayPin, LOW);
    }
  
    delay(500); // Delay for a short period to avoid rapid switching

}
