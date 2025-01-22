#include <Servo.h>
#include <Wire.h>
#include "Adafruit_TCS34725.h"

String status = "Nothing";

/* Initialise with specific int time and gain values */
Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_154MS, TCS34725_GAIN_1X);
Servo servoGate;
Servo servoRot;
Servo servoDump;

int state = 0;
int countR1 = 0;
int countR2 = 0;
int countR4 = 0;
int countA = 0;
int color = 0;

void setup(void) {
  Serial.begin(9600);
  pinMode(22, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(26, OUTPUT);
  pinMode(28, OUTPUT);
  pinMode(30, OUTPUT);
  
  if (tcs.begin()) {
    Serial.println("Found sensor");
  } else {
    Serial.println("No TCS34725 found ... check your connections");
    while (1);
  }

  servoGate.attach(3); //PWM pins
  servoRot.attach(4); //PWM pins
  servoDump.attach(10);
  servoRot.write(90);
  servoGate.write(180);
  servoDump.write(85);
}

void loop(void) {
  uint16_t r, g, b, c, colorTemp, lux;

  if (digitalRead(30) == HIGH){
    servoDump.write(13);
    Serial.println("Dumping");
    delay(1500);
    servoDump.write(87);
    delay(1500);
  }

  tcs.getRawData(&r, &g, &b, &c);
  // colorTemp = tcs.calculateColorTemperature(r, g, b);
  colorTemp = tcs.calculateColorTemperature_dn40(r, g, b, c);
  lux = tcs.calculateLux(r, g, b);
  // No ball: 0, Green: 1, Yellow: 2, Red: 3, Blue: 4
  if (lux < 50) {
    status = "No ball";
    color = 0;
    digitalWrite(22, LOW);
    digitalWrite(24, LOW);
    digitalWrite(26, LOW);
    digitalWrite(28, LOW);
  }
  else if (lux > 20000) {
    status = "red";
    color = 3;
    digitalWrite(22, HIGH);
    digitalWrite(24, LOW);
    digitalWrite(26, LOW);
    digitalWrite(28, LOW);
  }
  else if (r > 800) {
    status = "Yellow";
    color = 2;
    digitalWrite(22, LOW);
    digitalWrite(24, HIGH);
    digitalWrite(26, LOW);
    digitalWrite(28, LOW);
  }
  else if (g > 500) {
    status = "Green";
    color = 1;
    digitalWrite(22, LOW);
    digitalWrite(24, LOW);
    digitalWrite(26, LOW);
    digitalWrite(28, HIGH);
  }
  else {
    status = "Blue";
    color = 4;
    digitalWrite(22, LOW);
    digitalWrite(24, LOW);
    digitalWrite(26, HIGH);
    digitalWrite(28, LOW);
  }

  Serial.print("Lux: "); Serial.print(lux, DEC); Serial.print(" - ");
  Serial.print("R: "); Serial.print(r, DEC); Serial.print(" ");
  Serial.print("G: "); Serial.print(g, DEC); Serial.print(" ");
  Serial.print("B: "); Serial.print(b, DEC); Serial.print(" ");
  Serial.println(" ");
  Serial.println(status);
  
  delay(250);

  switch (state) {
    case 0: //start state
      //servoGate.write(0);
      //servoRot.write(0);
      if (countA == 4) {
        state = 1;
        countA = 0;
      }
      else if (countR1 == 4 || countR2 == 4 || countR4 == 4) {
        state = 2;
        countA = 0;
        countR1 = 0;
        countR2 = 0;
        countR4 = 0;
      }
      else {
        if (color == 1) {
          countR1 = countR1 + 1;
          countR2 = 0;
          countR4 = 0;
          countA = 0;
        }
        else if (color == 2) {
          countR1 = 0;
          countR2 = countR2 + 1;
          countR4 = countR4 + 1;
          countA = 0;
        }
        else if (color == 3) {
          countR1 = 0;
          countR2 = 0;
          countR4 = 0;
          countA = countA + 1;
        }
        else if (color == 4) {
          countR1 = 0;
          countR2 = 0;
          countR4 = countR4 + 1;
          countA = 0;
        }
        else {
          countR1 = 0;
          countR2 = 0;
          countA = 0;
        }
      }
      Serial.println("scanning");
      break;
    case 1: //Acceptance color detected
      Serial.println("accept");
      state = 0;
      servoGate.write(100);
      delay(1000);
      servoGate.write(180);
      //delay(1);

      break;
    case 2: //Rejection color detected
      Serial.println("reject");
      state = 0;
      servoRot.write(10);
      delay(500);
      servoGate.write(100);
      delay(1500);
      servoRot.write(90);
      servoGate.write(180);

      //delay(1);
      break;
  }
}
