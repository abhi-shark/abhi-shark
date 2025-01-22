
import serial
import serial.tools.list_ports
import time
from utilities import Motor, get_encoder_change, to_goal, wrap_to_pi, control_motors, scanSerial
from fsm import FSM
from qtpyControl import QTPYControl_1, QTPYControl_2
#from gpiozero import Button #may need rework or could bork it
import Encoder
import board
#import adafruit_bno055
import math
import RPi.GPIO as GPIO 

# TODO: nagivation
# TODO: motor code
# TODO: communications

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

def main():

    # Intialize QTPYs, represented as classes
    serport1 = "85438303233351815100"
    serport2 = "626DA1425154465336202020FF150C0B"

    for i in scanSerial():
        if i[2] == serport1:
            port1 = i[0]
        elif i[2] == serport2:
            port2 = i[0]
    
    ser1 = serial.Serial(port1, 9600)  
    ser2 = serial.Serial(port2, 9600)  


    QTPY1 = QTPYControl_1(ser1)
    QTPY2 = QTPYControl_2(ser2)

    """
    # Initialize IMU and I2C
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = adafruit_bno055.BNO055_I2C(i2c)
    """

    # Initialize FSM and associated variables
    fsm = FSM()
    pollen_count = 0
    prev_cs = 0
    fill_amount = 2  # specified number of pollen before moving
    sg = 0
    lr = 0
    plant3 = "None"

    # Initialize states
    # (x,y,yaw) = (0,0,0) defined as barn start pos
    # Assume relative ability to maintain straight line of motion, i.e. yaw = 0
    position = [0, 0, 0]
    timer = 0
    direction = 1  # direction of travel for encoder dist

    #Define barn and plant coords, NEU convention (bottom right is [0, 0])
    #home = [1.5, 1.5]
    #target = [4, 1.5]
    home = 0
    target = 100

    # Define input pins
    GPIO.setmode(GPIO.BCM) 
    START_GAME_PIN = 11
    

    # Initialize start game button
    GPIO.setup(START_GAME_PIN, GPIO.IN)

    # Initialize encoder variables
    PPR = 678 # encoder pulses per revolution, updated with testing
    wheel_radius = 32.5 # mm
    encoder1_pin1 = 5 # yellow wire
    encoder1_pin2 = 6 # green wire 
    encoder2_pin1 = 13 # yellow wire
    encoder2_pin2 = 19 # green wire

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

    prev_time = time.time() # TODO: test this

    while True:

        current_time = time.time()
        
        # Receive serial data from each QTPY and update QTPY values
        response = QTPY1.serialPort.readline().decode().strip()
        QTPY1.handle_action(response)

        """  
        # Update IMU data
        raw_degrees = sensor.euler[0]
        heading = raw_degrees*math.pi/180
        position[2] = wrap_to_pi(heading)
        """

        # Position update
        value_1 = encoder1.read()
        value_2 = encoder2.read()
        d = get_encoder_change(value_1, value_2, PPR, PPR, wheel_radius, wheel_radius)
        # position[0] = position[0] + d*math.cos(heading)
        # position[1] = position[1] +d*math.sin(heading)
        position = -d
        print(position)
        # Update with new sensor readings
        lr = lr  # Updated at last step, include here for redundancy
        ps = QTPY1.ps
        cs = QTPY1.cs

        if not sg:
            # Only read the start game button once, then sg is just based on timer
            sg = GPIO.input(START_GAME_PIN)
            
            # Set plant 2 color
            response = QTPY2.serialPort.readline().decode().strip()
            QTPY2.handle_action(response)
            QTPY1.color = QTPY2.color
            print("Set plant color to ", QTPY1.color)

        else:
            print(timer)
            sg = (timer <= 30)  # Time is less than two minutes

        # Calculate other inputs
        
        np = (pollen_count >= 0)
        fp = (pollen_count >= fill_amount)
        print("fp:", fp)

        # Update state
        fsm.update(ps, cs, lr, sg, np, fp)
        
        # Perform actions based on fsm output
        if fsm.tp:
            goal = target
            timer = timer + (current_time - prev_time)
            QTPY2.set_status("go")
            [left,right,direction,success] = to_goal(position, goal) 
            control_motors(left_motor, right_motor,direction,left,right) 
            lr = success
        elif fsm.hp:
            goal = home
            timer = timer + (current_time - prev_time)
            QTPY2.set_status("go")
            [left,right,direction,success]= to_goal(position, goal) 
            control_motors(left_motor, right_motor, direction, 0.9, 0.9) 
            #control_motors(left_motor, right_motor, direction, 0.0, 0.0) # test condition
            lr = success
        elif fsm.pd:
            control_motors(left_motor, right_motor, direction, 0.0, 0.0)
            time.sleep(1)
            QTPY1.actuate_servo("dis")
            timer = timer + (current_time - prev_time)
            QTPY2.set_status("go")
            pollen_count = 0
            time.sleep(1)
        elif fsm.rp:
            QTPY1.actuate_servo("rej")
            QTPY2.set_status("sort")
        elif fsm.ap:
            QTPY1.actuate_servo("acc")
            QTPY2.set_status("sort")
            pollen_count = pollen_count + 1

        if fsm.state == "done":
            # explicitly check for state to get around !sg
            QTPY2.set_status("stop")
            break

        # Update previous values
        prev_cs = cs
        prev_time = current_time
        prev_value1 = encoder1.read()
        prev_value2 = encoder2.read()

        time.sleep(0.5)


if __name__ == '__main__':
    main()


