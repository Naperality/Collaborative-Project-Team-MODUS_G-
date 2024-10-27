#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64  // OLED display height, in pixels
#define OLED_ADDR 0x3C   // I2C address for the OLED display

// Create an instance of the display
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  Serial.begin(9600);
  // Initialize the display
  display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR); // Initialize with I2C address
  display.clearDisplay(); // Clear the display buffer
    display.display(); // Show the text on the display


  
  
}

void loop() {
  // You can add more code here if needed
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n'); // Read the command until newline
    command.trim();
    
    display.clearDisplay();
 
    display.setTextSize(1); // Normal 1:1 pixel scale
    display.setTextColor(SSD1306_WHITE); // White text
    display.setCursor(0, 0); // Start at top-left corner
    display.println(command); // Print the input variable
    display.display();
    
    
  }
}