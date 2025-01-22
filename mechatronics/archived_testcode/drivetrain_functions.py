import RPi.GPIO as GPIO 
from gpiozero import RotaryEncoder 
import time 

 

# Define GPIO pins for motor control 

motor1_pwm_pin = 18  # PWM pin for motor 1 
motor1_dir_pin1 = 23  # Direction pin 1 for motor 1 
motor1_dir_pin2 = 24  # Direction pin 2 for motor 1 

motor2_pwm_pin = 17  # PWM pin for motor 2 
motor2_dir_pin1 = 27  # Direction pin 1 for motor 2 
motor2_dir_pin2 = 22  # Direction pin 2 for motor 2 

# Define GPIO pins for encoder1 
encoder1_pin1 = 5  # Encoder 1 pin 1 
encoder1_pin2 = 6  # Encoder 1 pin 2 

# Define GPIO pins for encoder2 
encoder2_pin1 = 13  # Encoder 2 pin 1 
encoder2_pin2 = 19  # Encoder 2 pin 2 

# Setup GPIO pins 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(motor1_pwm_pin, GPIO.OUT) 
GPIO.setup(motor1_dir_pin1, GPIO.OUT) 
GPIO.setup(motor1_dir_pin2, GPIO.OUT) 
GPIO.setup(motor2_pwm_pin, GPIO.OUT) 
GPIO.setup(motor2_dir_pin1, GPIO.OUT) 
GPIO.setup(motor2_dir_pin2, GPIO.OUT) 
pwm1 = GPIO.PWM(motor1_pwm_pin, 1000) 
pwm2 = GPIO.PWM(motor2_pwm_pin, 1000) 

# Setup GPIO pins for encoder 1 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(encoder1_pin1, GPIO.IN) 
GPIO.setup(encoder1_pin2, GPIO.IN) 

# Setup GPIO pins for encoder 2 
GPIO.setup(encoder2_pin1, GPIO.IN) 
GPIO.setup(encoder2_pin2, GPIO.IN) 

# Global variables to keep track of encoder counts 
encoder1_count = 0 
encoder2_count = 0 

#---------------------------------------------------------------------------------------------------------------------------
  #motor1/2_dir indicates which motor is currently being driven. It can be 0,1,2: 0 indicates reverse (CW) movement; 1 indicates no movement; 2 indicates forward movement (CCW) 

#speed1/2 indicates the speed of motors 1 and 2 respectively. max rated speed is 3.5m/s at 100% duty cycle. speed is a float between 0 and 100 indicating duty cycle resulting in speeds between 0 and 3.5 m/s 

def control_motor1(motor1_dir, speed1): 

    if motor1_dir == 2: 
        GPIO.output(motor1_dir_pin1, GPIO.HIGH) 
        GPIO.output(motor1_dir_pin2, GPIO.LOW) 
        pwm1.start(speed1) 
    elif motor1_dir == 0: 
        GPIO.output(motor1_dir_pin1, GPIO.LOW) 
        GPIO.output(motor1_dir_pin2, GPIO.HIGH) 
        pwm1.start(speed1) 

    else: 
        GPIO.output(motor1_dir_pin1, GPIO.LOW) 
        GPIO.output(motor1_dir_pin2, GPIO.LOW) 
        pwm1.stop() 

     

def control_motor2(motor2_dir, speed2): 

    if motor2_dir == 2: 
        GPIO.output(motor2_dir_pin1, GPIO.HIGH) 
        GPIO.output(motor2_dir_pin2, GPIO.LOW) 
        pwm2.start(speed2) 
    elif motor2_dir == 0: 
        GPIO.output(motor2_dir_pin1, GPIO.LOW) 
        GPIO.output(motor2_dir_pin2, GPIO.HIGH) 
        pwm2.start(speed2) 
    else: 
        GPIO.output(motor2_dir_pin1, GPIO.LOW) 
        GPIO.output(motor2_dir_pin2, GPIO.LOW) 
        pwm2.stop() 


#----------------------------------------------------------------------------------------------------------------------------- 

# Define Pulses Per Revolution (PPR) for the encoders 
PPR = 440 

# Define radius of the wheel connected to the encoder (in mm) 
wheel_radius = 32.5 

# Create instances of RotaryEncoder for encoder1 and encoder2 
encoder1 = RotaryEncoder(encoder1_pin1, encoder1_pin2, max_steps=PPR) 
encoder2 = RotaryEncoder(encoder2_pin1, encoder2_pin2, max_steps=PPR) 

# Initialize variables to keep track of previous encoder values 
prev_value1 = encoder1.value 
prev_value2 = encoder2.value 

# Function to calculate distance traveled by encoder 
def calculate_distance(pulses, PPR, radius): 
    # Calculate distance in mm 
    distance_mm = (2 * 3.14159 * radius * pulses) / PPR 
    return distance_mm 

try: 
    while True: 
        # Calculate change in encoder values 
        delta1 = encoder1.value - prev_value1 
        delta2 = encoder2.value - prev_value2 

        # Update previous values 
        prev_value1 = encoder1.value 
        prev_value2 = encoder2.value 

        # Calculate distance traveled by each encoder 
        distance1 = calculate_distance(delta1, PPR, wheel_radius) 
        distance2 = calculate_distance(delta2, PPR, wheel_radius) 

        # Print distance traveled by each encoder 
        print("Encoder 1 Distance:", distance1, "mm") 
        print("Encoder 2 Distance:", distance2, "mm") 

        # Wait for a short duration 
        time.sleep(0.1) 

 

except KeyboardInterrupt: 
    pass 

 

# Clean up GPIO resources 

encoder1.close() 
encoder2.close() 
 
