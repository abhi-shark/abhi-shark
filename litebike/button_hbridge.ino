//This is test code to demonstrate functionality
//Using an L298N H-bridge/DC motor combo instead of a stepper motor for actuation
//and simulating RFID input with a button input instead

#define BUTTON_PIN 3         // Pin for the button
#define MOTOR_PIN_FORWARD 9  // L298N IN1
#define MOTOR_PIN_BACKWARD 10 // L298N IN2
#define MOTOR_SPEED_PIN 6    // L298N ENA (PWM for speed control)

byte lastButtonState = HIGH; // Button state (HIGH = not pressed due to pull-up)
unsigned long debounceDuration = 50; // Debounce time in milliseconds
unsigned long lastButtonPressTime = 0;
unsigned long ignoreButtonPressDuration = 6000; // Ignore presses for 6 seconds
unsigned long motorHoldDuration = 4000;         // Hold time for 4 seconds

bool motorReturning = false;
unsigned long motorStartTime = 0;

void setup() {
  pinMode(BUTTON_PIN, INPUT_PULLUP); // Button with internal pull-up
  pinMode(MOTOR_PIN_FORWARD, OUTPUT);
  pinMode(MOTOR_PIN_BACKWARD, OUTPUT);
  pinMode(MOTOR_SPEED_PIN, OUTPUT);

  stopMotor(); // Ensure motor is off at startup
}

void loop() {
  // Read button state with debounce logic
  byte buttonState = digitalRead(BUTTON_PIN);
  if (buttonState != lastButtonState) {
    if (millis() - lastButtonPressTime > debounceDuration) {
      lastButtonPressTime = millis();

      // If button is pressed and action is not active
      if (buttonState == LOW && millis() - motorStartTime > ignoreButtonPressDuration) {
        motorStartTime = millis();
        motorReturning = true;

        // Run motor forward for 1 second
        runMotorForward();
        delay(1000);
        stopMotor();
      }
    }
  }
  lastButtonState = buttonState;

  // Check if motor needs to reverse after hold duration
  if (motorReturning && millis() - motorStartTime > motorHoldDuration) {
    motorReturning = false;

    // Run motor backward for 1 second
    runMotorBackward();
    delay(1000);
    stopMotor();
  }
}

void runMotorForward() {
  analogWrite(MOTOR_SPEED_PIN, 255); // Full speed (adjust for lower speed if needed)
  digitalWrite(MOTOR_PIN_FORWARD, HIGH);
  digitalWrite(MOTOR_PIN_BACKWARD, LOW);
}

void runMotorBackward() {
  analogWrite(MOTOR_SPEED_PIN, 255); // Full speed (adjust for lower speed if needed)
  digitalWrite(MOTOR_PIN_FORWARD, LOW);
  digitalWrite(MOTOR_PIN_BACKWARD, HIGH);
}

void stopMotor() {
  analogWrite(MOTOR_SPEED_PIN, 0); // Stop PWM
  digitalWrite(MOTOR_PIN_FORWARD, LOW);
  digitalWrite(MOTOR_PIN_BACKWARD, LOW);
}