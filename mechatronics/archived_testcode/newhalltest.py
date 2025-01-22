from gpiozero import RotaryEncoder
from signal import pause

# Create a RotaryEncoder object
encoder = RotaryEncoder(a=13, b=19)

# Initialize count variable
count = 0

# Define a callback function to handle rotation events
def rotate_handler(direction):
    global count
    if direction == 1:  # Clockwise rotation
        count += 1
    else:  # Counterclockwise rotation
        count -= 1
    print("Count:", count)

# Assign the callback function to the RotaryEncoder's rotation event
encoder.when_rotated(rotate_handler)

# Keep the program running
pause()
