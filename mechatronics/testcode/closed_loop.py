# Open loop control with TIME-BASED control
import time
from utilities import Motor, get_encoder_change, to_goal, wrap_to_pi, control_motors
import Encoder
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BCM)

# Initialize states
# (x,y,yaw) = (0,0,0) defined as barn start pos
# Assume relative ability to maintain straight line of motion, i.e. yaw = 0
position = [0, 0, 0]
timer = 0
direction = 1  # direction of travel for encoder dist

#Define barn and plant coords, NEU convention (bottom right is [0, 0])
home = [1.5, 1.5]
target = [4, 1.5]

# Set motor pin values
left_motor_pwm = 18
left_motor_pinA = 23
left_motor_pinB = 24
right_motor_pwm = 12
right_motor_pinA = 27
right_motor_pinB = 22

GPIO.setup(left_motor_pwm, GPIO.OUT)
GPIO.setup(right_motor_pwm, GPIO.OUT)
GPIO.setup(left_motor_pinA, GPIO.OUT)
GPIO.setup(left_motor_pinB, GPIO.OUT)
GPIO.setup(right_motor_pinA, GPIO.OUT)
GPIO.setup(right_motor_pinB, GPIO.OUT)

# Create motor objects
pwm1 = GPIO.PWM(left_motor_pwm, 1000) 
pwm2 = GPIO.PWM(right_motor_pwm, 1000) 

left_motor = Motor(left_motor_pwm, left_motor_pinA, left_motor_pinB, pwm1)
right_motor = Motor(right_motor_pwm, right_motor_pinA, right_motor_pinB, pwm2)

wheel_radius_1 = 32.5 
wheel_radius_2 = 32.5
PPR_1 = 678 
PPR_2 = 678

enc_1 = Encoder.Encoder(5,6)
enc_2 = Encoder.Encoder(13,19)


start_time = time.time()
elaps_time = 0

def get_encoder_change(pulses1, pulses2, PPR1, PPR2, radius1, radius2):
    distance1 = (2 * 3.14159 * radius1 * pulses1) / PPR1 # Distance of encoder 1 in mm
    distance2 = (-2 * 3.14159 * radius2 * pulses2) / PPR2 # Distance of encoder 2 in mm
    dx_average = (distance1 + distance2)/2 # Average of the two encoder distances
    print(dx_average)

    return dx_average


value_1 = enc_1.read()
value_2 = enc_2.read()
distance = get_encoder_change(value_1, value_2, PPR_1, PPR_2, wheel_radius_1, wheel_radius_2)


while distance < 300:
    # # Update IMU data
    # raw_degrees = sensor.euler[0]
    # heading = raw_degrees*math.pi/180
    # position[2] = wrap_to_pi(heading)

    # # Position update
    # delta1 = encoder1.value - prev_value1
    # delta2 = encoder2.value - prev_value2
    # d = get_encoder_change(delta1, delta2, PPR, wheel_radius)
    # position[0] = position[0] + d*math.cos(heading)
    # position[1] = position[1] +d*math.sin(heading)

    left = 0.9
        
    right = 0.9
    direction = -1

    control_motors(left_motor, right_motor,direction,left,right)
    value_1 = enc_1.read()
    value_2 = enc_2.read()
    distance = get_encoder_change(value_1, value_2, PPR_1, PPR_2, wheel_radius_1, wheel_radius_2)

left = 0
right = 0
direction = 0

control_motors(left_motor, right_motor,direction,left,right)
time.sleep(1)


while distance > 0:
    # Update IMU data
    # raw_degrees = sensor.euler[0]
    # heading = raw_degrees*math.pi/180
    # position[2] = wrap_to_pi(heading)

    # # Position update
    # delta1 = encoder1.value - prev_value1
    # delta2 = encoder2.value - prev_value2
    # d = get_encoder_change(delta1, delta2, PPR, wheel_radius)
    # position[0] = position[0] + d*math.cos(heading)
    # position[1] = position[1] +d*math.sin(heading)
    # print(position)
    left = 0.9
    right = 0.9
    direction = 1

    control_motors(left_motor, right_motor,direction,left,right)
    value_1 = enc_1.read()
    value_2 = enc_2.read()
    distance = get_encoder_change(value_1, value_2, PPR_1, PPR_2, wheel_radius_1, wheel_radius_2)
