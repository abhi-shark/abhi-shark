import RPi.GPIO as GPIO 
from gpiozero import RotaryEncoder 
import time 

# Define GPIO pins for encoder1 
encoder1_pin1 = 5  # Encoder 1 pin 1 
encoder1_pin2 = 6  # Encoder 1 pin 2 

# Define GPIO pins for encoder2 
encoder2_pin1 = 13  # Encoder 2 pin 1 
encoder2_pin2 = 19  # Encoder 2 pin 2 

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

# Define Pulses Per Revolution (PPR) for the encoders 
PPR = 440 

# Define radius of the wheel connected to the encoder (in mm) 
wheel_radius = 32.5 

# Create instances of RotaryEncoder for encoder1 and encoder2 
encoder1 = RotaryEncoder(encoder1_pin1, encoder1_pin2) 
encoder2 = RotaryEncoder(encoder2_pin1, encoder2_pin2) 

# Initialize variables to keep track of previous encoder values 
prev_value1 = encoder1.value 
prev_value2 = encoder2.value 



# Function to calculate distance traveled by encoder 
def calculate_distance(pulses, PPR, radius): 
    # Calculate distance in mm 
    distance_mm = (2 * 3.14159 * radius * pulses) / PPR 
    return distance_mm 


runenc = True

try: 
    while runenc: 
        # Calculate change in encoder values 
        delta1 = encoder1.value - prev_value1 
        delta2 = encoder2.value - prev_value2 

        # Update previous values 
        prev_value1 = encoder1.value 
        prev_value2 = encoder2.value 

        # Calculate distance traveled by each encoder 
        distance1 = calculate_distance(delta1, PPR, wheel_radius) 
        distance2 = calculate_distance(delta2, PPR, wheel_radius) 
        
        runenc = (abs(distance1) != 20)

        # Print distance traveled by each encoder 
        print("Encoder 1 Distance:", distance1, "mm") 
        print("Encoder 2 Distance:", distance2, "mm") 

        # Wait for a short duration 
        time.sleep(0.1) 

 

except KeyboardInterrupt: 
    pass 
