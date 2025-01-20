#include <SPI.h>
#include <MFRC522.h>
#include <Stepper.h>

// RFID Module Pins
#define RST_PIN 9  // Reset pin for RC522
#define SS_PIN 10  // Slave select pin for RC522 (SDA)

// Stepper Motor Configuration
#define STEPS_PER_REV 2048  // Steps per revolution for 28BYJ-48
Stepper stepperMotor(STEPS_PER_REV, 8, 7, 9, 11); // IN1, IN3, IN2, IN4 pins

// Timing Variables
unsigned long lastActivationTime = 0;
const unsigned long ignoreDuration = 6000; // Ignore RFID input for 6 seconds

MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();            // Initialize SPI bus
  mfrc522.PCD_Init();     // Initialize RC522
  stepperMotor.setSpeed(10); // Set speed of stepper motor (RPM)

  Serial.println("Place your RFID tag near the reader.");
}

void loop() {
  // Check for a new card
  if (millis() - lastActivationTime > ignoreDuration && 
      mfrc522.PICC_IsNewCardPresent() && 
      mfrc522.PICC_ReadCardSerial()) {
        
    Serial.println("RFID Tag detected!");

    // Rotate motor 90° clockwise
    stepperMotor.step(STEPS_PER_REV / 4); // 90 degrees = 1/4 revolution
    delay(4000);                         // Hold for 4 seconds

    // Rotate motor back to original position
    stepperMotor.step(-STEPS_PER_REV / 4); // -90 degrees = back to original

    // Update last activation time
    lastActivationTime = millis();

    // Halt the RFID card to prevent re-reading
    mfrc522.PICC_HaltA();
  }
}