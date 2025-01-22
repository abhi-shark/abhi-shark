import math
import RPi.GPIO as GPIO 
import serial

class Motor:
    def __init__(self, pwm_pin, pinA, pinB, pwm):
        self.pwm_pin = pwm_pin
        self.pinA = pinA
        self.pinB = pinB
        self.pwm = pwm

'''
def get_encoder_change(pulses1, pulses2, PPR, radius):
    distance1 = (2 * 3.14159 * radius * pulses1) / PPR # Distance of encoder 1 in mm
    distance2 = (2 * 3.14159 * radius * pulses2) / PPR # Distance of encoder 2 in mm
    dx_average = (distance1 + distance2)/2 # Average of the two encoder distances

    return dx_average/304.8
'''
   
def get_encoder_change(pulses1, pulses2, PPR1, PPR2, radius1, radius2):
    distance1 = (2 * 3.14159 * radius1 * pulses1) / PPR1 # Distance of encoder 1 in mm
    distance2 = (2 * 3.14159 * radius2 * pulses2) / PPR2 # Distance of encoder 2 in mm
    dx_average = (distance1 + distance2)/2 # Average of the two encoder distances
    #print(dx_average)
    dx_avg_scaled = dx_average*26.5/155

    return dx_avg_scaled

def to_goal_pcontrol(position, goal):
    """
    Outputs cmd signal from 0 to 1 
    for the left and right wheels.
    Also outputs boolean lr if the position is
    within distance of the goal"""

    # TODO: check cmd value????
    left = 1
    right = 1

    # Control parameters
    Kp = 1.0
    Kl = 1.0
    Kr = 1.0
    avgPower = 20

    yaw_des = math.atan2(goal[1] - position[1], goal[0] - position[0])
    yaw = position[2]
    u = Kp*wrap_to_pi(yaw_des - yaw)

    uL = max(0.0,min(255.0,(avgPower - u)*Kl))
    uR = max(0.0,min(255.0,(avgPower + u)*Kr))

    dx = goal[0] - position[0]
    dy = goal[1] - position[1]
    
    dist = math.sqrt(dx^2 + dy^2)

    lr = (abs(dist)<0.05)

    return [left, right, lr]

def to_goal(position, goal):
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
    left = 0.4
    right = 0.4
    success = (abs(goal-position) <= 0.05)

    return [left,right,direction,success]

def control_motors(left_motor, right_motor, direction, left_speed, right_speed):
    """
    left_motor, right_motor: Motor() objects
    direction: 1 for forward, -1 for reverse
    left_speed, right_speed: cmd signal between 0 and 100, representing a speed
    """
    # Convert [0,1] command to range [1,100]
    left_speed = left_speed*100
    right_speed = right_speed*100

    if (left_speed > 90) or (right_speed > 90):
        # Add safety condition to cap speed at 80
        left_speed = min(left_speed, 90)
        right_speed = min(right_speed, 90)
        
    if direction == 1: 
        GPIO.output(left_motor.pinA, GPIO.HIGH) 
        GPIO.output(left_motor.pinB, GPIO.LOW) 
        left_motor.pwm.start(left_speed) 
    elif direction == -1: 
        GPIO.output(left_motor.pinA, GPIO.LOW) 
        GPIO.output(left_motor.pinB, GPIO.HIGH) 
        left_motor.pwm.start(left_speed) 

    else: 
        GPIO.output(left_motor.pinA, GPIO.LOW) 
        GPIO.output(left_motor.pinB, GPIO.LOW) 
        left_motor.pwm.stop()

    if direction == 1: 
        GPIO.output(right_motor.pinA, GPIO.HIGH) 
        GPIO.output(right_motor.pinB, GPIO.LOW) 
        right_motor.pwm.start(right_speed) 
    elif direction == -1: 
        GPIO.output(right_motor.pinA, GPIO.LOW) 
        GPIO.output(right_motor.pinB, GPIO.HIGH) 
        right_motor.pwm.start(right_speed) 
    else: 
        GPIO.output(right_motor.pinA, GPIO.LOW) 
        GPIO.output(right_motor.pinB, GPIO.LOW) 
        right_motor.pwm.stop() 
    
    return 

def wrap_to_pi(angle):
    """Wrap angle data in radians to [-pi, pi]

    Parameters:
    angle (float)   -- unwrapped angle

    Returns:
    angle (float)   -- wrapped angle
    """
    while angle >= math.pi:
        angle -= 2*math.pi

    while angle <= -math.pi:
        angle += 2*math.pi
    return angle

def scanSerial() :
    output = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports) :
        # port, description, hwid string, and serial number
        try:
            output.append([port, hwid, hwid.split(" ")[2].split("=")[1]])
        except:
            continue
    return output
