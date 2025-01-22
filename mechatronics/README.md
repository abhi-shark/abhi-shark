## Organization of this GitHub Repository
- archived_testcode: old test files
- testcode: current testing files
- QTPY: Arduino code that runs on the QTPY microcontrollers
- Other code not in folders: main Python code to be run on the central microprocessor

## Running Code on RPi
1. Connect to power
2. MUST BE CONNECTED TO HOTSPOT- both the laptop AND pi
3. Open SSH terminal (i.e. MobaXTerm) - Do not check default user, or do and specify "pi" as user
4. UN: pi, PW: bird
5. IP: specified in group chat
6. If IP addr isn't working for some reason, connect to monitor, go to wifi button thing and go to connection details/settings and look for IP address - or hover over wifi icon on the desktop with the mouse and it will show you the IP
9. Once activated, you will see a terminal with something like `pi@mered/~ $`
10. Type in `source me588/bin/activate` and enter to start a Python virtual environment- this makes it so you can install packages and do anything you could normally do in Python. Technically you don't need to do this every time if you're not installing or modifying things but it is safe to do so.
11. `cd Desktop/ME588` to get to the proper location of main.py 
12. Type `python main.py` to run the file

### to verify if device is at /dev/ttyACM0, run:
`udevadm info -a -p  $(udevadm info -q path -n /dev/ttyACM0)`
## General Hierarchy
# Central computer:
    INPUTS:
        - Wheel encoder inputs (2)
        - Start button
    
    OUTPUTS:
        - Motor PWM (2) --> tp and hp
        - LED for accept/reject
    
# Peripheral (QTPY) 1:
    INPUTS:
        - Color sensor
        - Ultrasonic sensor?
    
    OUTPUTS:
        - Actuate servos (3) --> pd, rp, ap
        
    SERIAL OUTPUT:
        - Color data (as string)
        - Ultrasonic data?
    
# Peripheral (QTPY) 2: 
    INPUTS:
        - Encoder color inputs (3)
    
    OUTPUTS:
        - RGB leds (3) for plant color
        - RBG leds (1) for current game status
    
    SERIAL OUTPUT:
        - Plant 3 color
