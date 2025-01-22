# Tests just the motor function

import RPi.GPIO as GPIO 
import time 
# from drivetrain_functions import control_motor1

# Define GPIO pins for motor control 

motor1_pwm_pin = 18  # PWM pin for motor 1 
motor1_dir_pin1 = 23  # Direction pin 1 for motor 1 
motor1_dir_pin2 = 24  # Direction pin 2 for motor 1 

motor2_pwm_pin = 12  # PWM pin for motor 2 
motor2_dir_pin1 = 27  # Direction pin 1 for motor 2 
motor2_dir_pin2 = 22  # Direction pin 2 for motor 2 



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



def control_motor1(motor1_dir, speed1): 

    if motor1_dir == 1: 
        GPIO.output(motor1_dir_pin1, GPIO.HIGH) 
        GPIO.output(motor1_dir_pin2, GPIO.LOW) 
        pwm1.start(speed1) 
    elif motor1_dir == -1: 
        GPIO.output(motor1_dir_pin1, GPIO.LOW) 
        GPIO.output(motor1_dir_pin2, GPIO.HIGH) 
        pwm1.start(speed1) 

    else: 
        GPIO.output(motor1_dir_pin1, GPIO.LOW) 
        GPIO.output(motor1_dir_pin2, GPIO.LOW) 
        pwm1.stop() 


def control_motor2(motor2_dir, speed2): 

    if motor2_dir == -1: 
        GPIO.output(motor2_dir_pin1, GPIO.HIGH) 
        GPIO.output(motor2_dir_pin2, GPIO.LOW) 
        pwm2.start(speed2) 
    elif motor2_dir == 1: 
        GPIO.output(motor2_dir_pin1, GPIO.LOW) 
        GPIO.output(motor2_dir_pin2, GPIO.HIGH) 
        pwm2.start(speed2) 
    else: 
        GPIO.output(motor2_dir_pin1, GPIO.LOW) 
        GPIO.output(motor2_dir_pin2, GPIO.LOW) 
        pwm2.stop() 

        

start_time = time.time()
elaps_time = 0

while elaps_time < 6:

    left = 0.5
    right = 0.5
    direction1 = 1

    control_motor1(direction, left)
    control_motor2(direction, right)
    elaps_time = time.time() - start_time

while elaps_time < 10:
    left = 0
    right = 0
    direction = -1

    control_motor1(direction, left)
    control_motor2(direction, right)
    elaps_time = time.time() - start_time

while elaps_time < 16:

    left = 0.5
    right = 0.5
    direction = -1

    control_motor1(direction, left)
    control_motor2(direction, right)
    elaps_time = time.time() - start_time
