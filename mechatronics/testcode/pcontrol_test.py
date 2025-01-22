import serial
import time
from utilities import motor, get_encoder_change, to_goal, wrap_to_pi, control_motors
from fsm import FSM
from qtpyControl import QTPYControl_1, QTPYControl_2
from gpiozero import Button
from gpiozero import RotaryEncoder
import board
import adafruit_bno055
import math
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

# Define input pins
START_GAME_PIN = 13

# Initialize IMU and I2C
i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Initialize start game button
button = Button(START_GAME_PIN)

# Initialize encoder variables
PPR = 440 # encoder pulses per revolution
wheel_radius = 32.5 # mm
encoder1_pin1 = 5 
encoder1_pin2 = 6 
encoder2_pin1 = 13
encoder2_pin2 = 19

# Create encoder objects
encoder1 = RotaryEncoder(encoder1_pin1, encoder1_pin2, max_steps=PPR)
encoder2 = RotaryEncoder(encoder2_pin1, encoder2_pin2, max_steps=PPR)

# Set initial encoder positions
prev_value1 = encoder1.value
prev_value2 = encoder2.value

# Set motor pin values
left_motor_pwm = 18
left_motor_pinA = 23
left_motor_pinB = 24
right_motor_pwm = 12
right_motor_pinA = 27
right_motor_pinB = 22

# Create motor objects
pwm1 = GPIO.PWM(left_motor_pwm, 1000) 
pwm2 = GPIO.PWM(right_motor_pwm, 1000) 

left_motor = motor(left_motor_pwm, left_motor_pinA, left_motor_pinB, pwm1)
right_motor = motor(right_motor_pwm, right_motor_pinA, left_motor_pinB, pwm2)

goal = target

while not lr:
    # Update IMU data
    raw_degrees = sensor.euler[0]
    heading = raw_degrees*math.pi/180
    position[2] = wrap_to_pi(heading)

    # Position update
    delta1 = encoder1.value - prev_value1
    delta2 = encoder2.value - prev_value2
    d = get_encoder_change(delta1, delta2, PPR, wheel_radius)
    position[0] = position[0] + d*math.cos(heading)
    position[1] = position[1] +d*math.sin(heading)

    [left, right, lr] = to_goal(position, goal)
    control_motors(left_motor, right_motor,direction,left,right)