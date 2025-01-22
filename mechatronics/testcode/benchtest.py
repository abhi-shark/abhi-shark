# Tests just the motor function

import RPi.GPIO as GPIO 
from gpiozero import RotaryEncoder 
import time 
# from drivetrain_functions import control_motor1

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

        
while True:
    control_motor1(2,50)
    control_motor2(2,50)
