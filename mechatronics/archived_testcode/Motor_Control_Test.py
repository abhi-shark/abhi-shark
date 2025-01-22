import RPi.GPIO as GPIO 
import time

# Define GPIO pins for motor control 

motor1_pwm_pin = 18  # PWM pin for motor 1 
motor1_dir_pin1 = 23  # Direction pin 1 for motor 1 
motor1_dir_pin2 = 24  # Direction pin 2 for motor 1 

motor2_pwm_pin = 12  # PWM pin for motor 2 
motor2_dir_pin1 = 27  # Direction pin 1 for motor 2 
motor2_dir_pin2 = 22  # Direction pin 2 for motor 2 

motor1_speed = 100 # Speed for motor1
motor2_speed = 100 # Speed for motor2

motor1_direction = 1 # 1 is forward, -1 is backward
motor2_direction = 1 # 1 is forward, -1 is backward

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

# Get initial time
initial_time = time.time()

while True:

  time_elapsed = time.time() - initial_time
  control_motor1(motor1_direction, motor1_speed)
  control_motor2(motor2_direction, motor2_speed)

  if time_elapsed >= 3:
    break

control_motor1(0, 0)
control_motor2(0, 0)

#---------------------------------------------------------------------------------------------------------------------------
  #motor1/2_dir indicates which motor is currently being driven. It can be 0,1,2: 0 indicates reverse (CW) movement; 1 indicates no movement; 2 indicates forward movement (CCW) 

#speed1/2 indicates the speed of motors 1 and 2 respectively. max rated speed is 3.5m/s at 100% duty cycle. speed is a float between 0 and 100 indicating duty cycle resulting in speeds between 0 and 3.5 m/s 

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

    if motor2_dir == 1: 
        GPIO.output(motor2_dir_pin1, GPIO.HIGH) 
        GPIO.output(motor2_dir_pin2, GPIO.LOW) 
        pwm2.start(speed2) 
    elif motor2_dir == -1: 
        GPIO.output(motor2_dir_pin1, GPIO.LOW) 
        GPIO.output(motor2_dir_pin2, GPIO.HIGH) 
        pwm2.start(speed2) 
    else: 
        GPIO.output(motor2_dir_pin1, GPIO.LOW) 
        GPIO.output(motor2_dir_pin2, GPIO.LOW) 
        pwm2.stop() 
