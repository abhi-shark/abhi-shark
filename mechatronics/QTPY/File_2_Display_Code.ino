#include <SPI.h>
#include <FastLED.h>

#define LED_PIN  8
#define NUM_LEDS  5

CRGB leds[NUM_LEDS];

String state_color = "STO";
bool accept = 0; // tells if pollen should be accepted or rejected

byte R = 0; // red value of LED
byte G = 0; // green value of LED
byte B = 0; // blue value of LED

String plant_3 = "NON"; //color of plant 3 as a string, will be sent back to the pi
bool set_color = 0;

int encoder_1 = 0; // turns on encoder for plant 1
int encoder_2 = 0; // turns on encoder for plant 2
int encoder_3 = 0; // turns on encoder for plant 3
int encoder_1_change = 0;
int encoder_2_change = 0;
int encoder_3_change = 0;
int ENC1_PINA = A0;
int ENC1_PINB = A1;
int ENC2_PINA = A2;
int ENC2_PINB = A3;
int ENC3_PINA = A6;
int ENC3_PINB = A7;

void setup() {
  // put your setup code here, to run once:
  pinMode(ENC1_PINA, INPUT);
  pinMode(ENC1_PINB, INPUT);
  pinMode(ENC2_PINA, INPUT);
  pinMode(ENC2_PINB, INPUT);
  pinMode(ENC3_PINA, INPUT);
  pinMode(ENC3_PINB, INPUT);

  FastLED.addLeds<WS2812,LED_PIN,GRB>(leds,NUM_LEDS);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    String sub = command.substring(0, 3); 
    if (sub == "SET") {
      set_color = 1;
    }
    else if ((sub == "STO") || (sub == "SOR") || (sub == "RUN")) {
      state_color = sub;
    }
  }

  // LED 1 code, indicated color of plant 1
  encoder_1_change = readEncoder1(ENC1_PINA, ENC1_PINB);
  if(encoder_1_change != 0){
    encoder_1 = encoder_1 + encoder_1_change;
  }
  if(abs(encoder_1) % 3 == 0){
    B = 255;
    G = 0;
    R = 0;
  }
  else if (abs(encoder_1) % 3 == 1){
    B = 0;
    G = 255;
    R = 0;
  }
  else{
    B = 0;
    G = 0;
    R = 255;
  }
  leds[0] = CRGB(R,G,B);

  // LED 2 code, indicated color of plant 2
  encoder_2_change = readEncoder2(ENC2_PINA, ENC2_PINB);
  if(encoder_2_change != 0){
    encoder_2 = encoder_2 + encoder_2_change;
  }
  if(abs(encoder_2) % 3 == 0){
    B = 255;
    G = 0;
    R = 0;
  }
  else if (abs(encoder_2) % 3 == 1){
    B = 0;
    G = 255;
    R = 0;
  }
  else{
    B = 0;
    G = 0;
    R = 255;
  }
  leds[1] = CRGB(R,G,B);

  // LED 3 code, indicated color of plant 3
  encoder_3_change = readEncoder3(ENC3_PINA, ENC3_PINB);
  if(encoder_3_change != 0){
    encoder_3 = encoder_3 + encoder_3_change;
  }
  if(abs(encoder_3) % 3 == 0){
    B = 255;
    G = 0;
    R = 0;
    plant_3 = "BLU";
  }
  else if (abs(encoder_3) % 3 == 1){
    B = 0;
    G = 255;
    R = 0;
    plant_3 = "GRN";
  }
  else{
    B = 0;
    G = 0;
    R = 255;
    plant_3 = "RED";
  }
  leds[2] = CRGB(R,G,B);

  // LED 4 code, indicates state of the robot
  // TODO: read color string from communication
  if(state_color == "STO"){
    B = 0;
    G = 0;
    R = 255;
    // TODO: Send plant 3 color through communication
  }
  else if(state_color == "SOR"){
    B = 0;
    G = 30;
    R = 255;
  }
  else{
    B = 0;
    G = 255;
    R = 0;
  }
  leds[3] = CRGB(R,G,B);

  // LED 5 code, indicated if pollen is being accepted or rejected
  // TODO: read reject from communication
  if(accept == 0){
    B = 0;
    G = 0;
    R = 255;
  }
  else{
    B = 0;
    G = 255;
    R = 0;
  }
  leds[4] = CRGB(R,G,B);
  FastLED.show();

  Serial.println(plant_3);
}

int readEncoder1(int chA1, int chB1) {
  // A function that reads the quadrature input from specified
  // pins and returns an encoder count change.
  
  // Create variable to return based on detected rotor rotation
  int result1 = 0;

  // Keep track of last switch state
  static int chA_last1 = digitalRead(chA1);
  static int chB_last1 = digitalRead(chB1);

  // Read the quadrature inputs
  int chA_new1 = digitalRead(chA1);
  int chB_new1 = digitalRead(chB1);

  // We look for Channel A to switch from LOW to HIGH
  if ((chA_last1 == LOW) && (chA_new1 == HIGH)) {
    // If Channel B is HIGH while Channel A goes 0->1, 
    // then the shaft is turning CW, and we should
    // increase the encoder count by 1. Otherwise it is
    // turning CCW, and we should decrease the encoder
    // count by 1.    
    if ((chB_last1 == HIGH) && (chB_new1 == HIGH)) { // CW turn
      result1 = 1;
    } 
    if ((chB_last1 == LOW) && (chB_new1 == LOW)) { // CW turn
      result1 = -1;
    } 
  }

  // Reassign prior Channel A value
  chA_last1 = chA_new1;
  chB_last1 = chB_new1;

  // Return encoder change
  return result1;
}

int readEncoder2(int chA2, int chB2) {
  // A function that reads the quadrature input from specified
  // pins and returns an encoder count change.
  
  // Create variable to return based on detected rotor rotation
  int result2 = 0;

  // Keep track of last switch state
  static int chA_last2 = digitalRead(chA2);
  static int chB_last2 = digitalRead(chB2);

  // Read the quadrature inputs
  int chA_new2 = digitalRead(chA2);
  int chB_new2 = digitalRead(chB2);

  // We look for Channel A to switch from LOW to HIGH
  if ((chA_last2 == LOW) && (chA_new2 == HIGH)) {
    // If Channel B is HIGH while Channel A goes 0->1, 
    // then the shaft is turning CW, and we should
    // increase the encoder count by 1. Otherwise it is
    // turning CCW, and we should decrease the encoder
    // count by 1.    
    if ((chB_last2 == HIGH) && (chB_new2 == HIGH)) { // CW turn
      result2 = 1;
    } 
    if ((chB_last2 == LOW) && (chB_new2 == LOW)) { // CW turn
      result2 = -1;
    } 
  }

  // Reassign prior Channel A value
  chA_last2 = chA_new2;
  chB_last2 = chB_new2;

  // Return encoder change
  return result2;
}

int readEncoder3(int chA3, int chB3) {
  // A function that reads the quadrature input from specified
  // pins and returns an encoder count change.
  
  // Create variable to return based on detected rotor rotation
  int result3 = 0;

  // Keep track of last switch state
  static int chA_last3 = digitalRead(chA3);
  static int chB_last3 = digitalRead(chB3);

  // Read the quadrature inputs
  int chA_new3 = digitalRead(chA3);
  int chB_new3 = digitalRead(chB3);

  // We look for Channel A to switch from LOW to HIGH
  if ((chA_last3 == LOW) && (chA_new3 == HIGH)) {
    // If Channel B is HIGH while Channel A goes 0->1, 
    // then the shaft is turning CW, and we should
    // increase the encoder count by 1. Otherwise it is
    // turning CCW, and we should decrease the encoder
    // count by 1.    
    if ((chB_last3 == HIGH) && (chB_new3 == HIGH)) { // CW turn
      result3 = 1;
    } 
    if ((chB_last3 == LOW) && (chB_new3 == LOW)) { // CW turn
      result3 = -1;
    } 
  }

  // Reassign prior Channel A value
  chA_last3 = chA_new3;
  chB_last3 = chB_new3;

  // Return encoder change
  return result3;
}