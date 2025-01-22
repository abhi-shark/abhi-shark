import RPi.GPIO as GPIO 
import time
# def main():
#   from gpiozero import Button
#   START_GAME_PIN = 2
#   button = Button(START_GAME_PIN)
#   while True:
#     if(sg = button.is_pressed):
#       print("hi")

def main():
  GPIO.setmode(GPIO.BCM) 
  START_GAME_PIN = 2
  
  GPIO.setup(START_GAME_PIN, GPIO.IN) 
  # TODO: can add a pull up or pull down resistor to that

  if GPIO.input(START_GAME_PIN):
    print('Input was HIGH')
  else:
      print('Input was LOW')
  time.sleep(0.5)
