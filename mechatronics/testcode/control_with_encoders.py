
# Open loop control with TIME-BASED control
import math
from utilities import Motor, get_encoder_change, to_goal, wrap_to_pi, control_motors
import Encoder
import RPi.GPIO as GPIO 
import time

# Initialize states
# (x,y,yaw) = (0,0,0) defined as barn start pos
# Assume relative ability to maintain straight line of motion, i.e. yaw = 0
position = 0
direction = 0  # direction of travel for encoder dist

# TODO: update this distance depending on how far you want to go. These are the two waypoints
waypoints = [300, 0]

# Initialize encoder variables
# TODO: change PPR?
PPR = 440 # encoder pulses per revolution
wheel_radius = 32.5 # mm
encoder1_pin1 = 5 
encoder1_pin2 = 6 
encoder2_pin1 = 13
encoder2_pin2 = 19

# Create encoder objects
encoder1 = Encoder.Encoder(encoder1_pin1, encoder1_pin2)
encoder2 = Encoder.Encoder(encoder2_pin1, encoder2_pin2)

# Set initial encoder positions
prev_value1 = encoder1.read()
prev_value2 = encoder2.read()

# Set motor pin values
left_motor_pwm = 18
left_motor_pinA = 23
left_motor_pinB = 24
right_motor_pwm = 12
right_motor_pinA = 27
right_motor_pinB = 22

# Setup GPIO pins 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(left_motor_pwm, GPIO.OUT) 
GPIO.setup(left_motor_pinA, GPIO.OUT) 
GPIO.setup(left_motor_pinB, GPIO.OUT) 
GPIO.setup(right_motor_pwm, GPIO.OUT) 
GPIO.setup(right_motor_pinA, GPIO.OUT) 
GPIO.setup(right_motor_pinB, GPIO.OUT)

pwm1 = GPIO.PWM(left_motor_pwm, 1000) 
pwm2 = GPIO.PWM(right_motor_pwm, 1000) 

# Create motor objects
left_motor = Motor(left_motor_pwm, left_motor_pinA, left_motor_pinB, pwm1)
right_motor = Motor(right_motor_pwm, right_motor_pinA, right_motor_pinB, pwm2)


# TODO: what is the 304.8?
def get_encoder_change(pulses1, pulses2, PPR1, PPR2, radius1, radius2,direction):
    distance1 = (2 * 3.14159 * radius1 * pulses1) / PPR1 # Distance of encoder 1 in mm
    distance2 = (2 * 3.14159 * radius2 * pulses2) / PPR2 # Distance of encoder 2 in mm
    dx_average = direction*(distance1 + distance2)/2 # Average of the two encoder distances
    #print(dx_average)

    return dx_average

# TODO: check if yall agree with this logic
# trying to mimic the actual behavior by stopping for 5 seconds, then reversing motor direction
def stupid_control(position, goal):
    """
    Takes a distance (one dimensional),
    checks if it is within some desired distance,
    and executes the desired behavior (ideally)
    Direction is determined by the sign of the dist 
    to the goal
    cmd signal (left and right) is hardcoded to
    0.5 for both motors"""
    if (goal-position) >= 0:
        direction = -1
    else:
        direction = 1
    left = 0.3
    right = 0.3
    success = (abs(goal-position) <= 50)

    return [left,right,direction,success]

for wp in waypoints:
    success = 0
    while not success:
        goal = wp
        print(goal-position)
        # Position update
        value_1 = encoder1.read()
        value_2 = encoder2.read()
        d = get_encoder_change(value_1, value_2, PPR, PPR, wheel_radius, wheel_radius, direction)
        position = d
        print(position)

        # Determine cmd output
        [left,right,direction,success] = stupid_control(position,goal)

        # Pass cmd to motors
        control_motors(left_motor, right_motor,direction,left,right)
    # TODO: here's that pause
    print(success)
    control_motors(left_motor,right_motor,direction,0,0)
    time.sleep(1)

# Shut down motors?
# TODO: get rid of this if this is bad to do
control_motors(left_motor, right_motor,direction,0,0)
