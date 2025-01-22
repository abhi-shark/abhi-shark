# Open loop control with TIME-BASED control
import time
from utilities import Motor, get_encoder_change, to_goal, wrap_to_pi, control_motors
import Encoder
import RPi.GPIO as GPIO 

# Initialize states
# (x,y,yaw) = (0,0,0) defined as barn start pos
# Assume relative ability to maintain straight line of motion, i.e. yaw = 0
position = [0, 0, 0]
timer = 0
direction = 1  # direction of travel for encoder dist

#Define barn and plant coords, NEU convention (bottom right is [0, 0])
home = [1.5, 1.5]
target = [4, 1.5]

# Define GPIO pins for motor control 

motor1_pwm_pin = 18  # PWM pin for motor 1 
motor1_dir_pin1 = 23  # Direction pin 1 for motor 1 
motor1_dir_pin2 = 24  # Direction pin 2 for motor 1 

motor2_pwm_pin = 12  # PWM pin for motor 2 
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

left_motor = Motor(motor1_pwm_pin, motor1_dir_pin1, motor1_dir_pin2, pwm1)
right_motor = Motor(motor2_pwm_pin, motor2_dir_pin1, motor2_dir_pin2, pwm2)


start_time = time.time()
elaps_time = 0

while elaps_time < 6:

    left = 0.5
    right = 0.5
    direction = 1

    control_motors(left_motor, right_motor,direction,left,right)
    elaps_time = time.time() - start_time

while elaps_time < 10:
    left = 0
    right = 0
    direction = -1

    control_motors(left_motor, right_motor,direction,left,right)
    elaps_time = time.time() - start_time

while elaps_time < 16:

    left = 0.5
    right = 0.5
    direction = -1

    control_motors(left_motor, right_motor,direction,left,right)
    elaps_time = time.time() - start_time