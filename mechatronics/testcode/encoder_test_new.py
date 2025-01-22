import Encoder

# Define Pulses Per Revolution (PPR) for the encoders 
PPR_1 = 440 
PPR_2 = 440 

# Define radius of the wheel connected to the encoder (in mm) 
wheel_radius_1 = 32.5 
wheel_radius_2 = 32.5 

# REPLACE THE PINS WITH THE ACTUAL ENCODER PINS SORRY IM PRESSED FOR TIME
enc_1 = Encoder.Encoder(5,6)
enc_2 = Encoder.Encoder(13,19)

value_1 = enc_1.read() #TODO: i think this is the right command hut cant remmwbwr. check file that is on raspberry pi
value_2 = enc_2.read()



def get_encoder_change(pulses1, pulses2, PPR1, PPR2, radius1, radius2):
    distance1 = (2 * 3.14159 * radius1 * pulses1) / PPR1 # Distance of encoder 1 in mm
    distance2 = (-2 * 3.14159 * radius2 * pulses2) / PPR2 # Distance of encoder 2 in mm
    dx_average = (distance1 + distance2)/2 # Average of the two encoder distances

    return dx_average/304.8, distance1/304.8, distance2/304.8
  
try: 
    while true: 
      get_encoder_change(value_1, value_2, PPR_1, PPR_2, wheel_radius_1, wheel_radius_2)
      print(distance1)
      print(distance2)
except KeyboardInterrupt: 
    pass 


"""
FYI you should check this out, seems to be good

https://learn.adafruit.com/rotary-encoder/circuitpython
"""
