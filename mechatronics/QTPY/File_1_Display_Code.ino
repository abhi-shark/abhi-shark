#include "Adafruit_TCS34725.h"
#include <Servo.h>

#define THRESHOLD 60

Adafruit_TCS34725 tcs = Adafruit_TCS34725(TCS34725_INTEGRATIONTIME_101MS, TCS34725_GAIN_4X);

Servo servoGate;
Servo servoRot;
Servo servoDump;

word lux = 0;
byte B = 0;
byte G = 0;
byte R = 0;
byte brightness = 0;

String color = "NON";

const int GATE_PIN = 0; // set pin number
const int ROT_PIN = 2; // set pin numnber
const int DUMP_PIN = 1; // set pin number
int countA = 0;
int countR1 = 0;
int countR2 = 0;
int countR3 = 0;

//int trigpin = // set the trigger pin number
//int echopin = // set the echo pin number

void setup() {
  // put your setup code here, to run once:
  tcs.begin();

  servoGate.attach(GATE_PIN); 
  servoRot.attach(ROT_PIN); 
  servoDump.attach(DUMP_PIN);
  servoRot.write(90);
  servoGate.write(180);
  servoDump.write(85);

  //pinMode(trigpin, OUTPUT);
  //pinMode(echopin, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  uint16_t r, g, b, c, colorTemp, lux;

  tcs.getRawData(&r, &g, &b, &c);
  // colorTemp = tcs.calculateColorTemperature(r, g, b);
  colorTemp = tcs.calculateColorTemperature_dn40(r, g, b, c);
  lux = tcs.calculateLux(r, g, b);

  if (lux < 50) {
    color = "NON";
  }
  else if (lux > 20000) {
    color = "RED";
  }
  // else if (r > 1600) {
  //   color = "YEL";
  // }
  else if (g > 1000) {
    color = "GRE";
  }
  else {
    color = "BLU";
  }

  /*
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  */

  //TODO: output distance or duration value

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command from the QTPy
    String sub = command.substring(0, 3); // Parse the first three characters into a substring

    if (sub == "ACC") {
      servoGate.write(100);
      delay(1000);
      servoGate.write(180);
    }

    if (sub == "REJ") {
      servoRot.write(10);
      delay(500);
      servoGate.write(100);
      delay(1500);
      servoRot.write(90);
      servoGate.write(180);
    }

    if (sub == "DIS") {
      servoDump.write(13);
      delay(1500);
      servoDump.write(87);
      delay(1500);
    }
  }

  delay(1000);
  Serial.println(color);

}
