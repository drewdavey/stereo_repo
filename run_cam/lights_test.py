import time
from picamera2 import Picamera2
from gpiozero import Factory, Button, LED
from signal import pause
import subprocess
from settings import *
from datetime import datetime, timezone
from time import sleep

right_button = Button(18, hold_time=3)  
left_button = Button(17, hold_time=3)

green = LED(12)

green.on()
sleep(1)
green.close()
sleep(1)
AK = LED(12)
AK.on()
sleep(1)
# while not process.poll() is None:  # Check if standby.py is still running
#     right_button = Button(18, hold_time=5) 
#     left_button = Button(17, hold_time=5)
#     if (right_button.is_held and left_button.is_held):
#         green.close()
#         right_button.close()
#         left_button.close()
#         exit()

# def enter_standby(fdir, fname_log, dt, num_frames):
#     process = subprocess.Popen(['python3', 'standby.py', fdir, fname_log, str(dt), str(num_frames)])
#     return process

while True:
    if (right_button.is_held and left_button.is_held): 
        green.close()
        # right_button.close()
        # left_button.close() 
        time.sleep(1)
        process = subprocess.Popen(['python3', 'sub_lights.py', right_button, left_button])
        # time.sleep(1)
        process.wait()
        # GPIO.cleanup()
        # right_button = Button(18, hold_time=3)  
        # left_button = Button(17, hold_time=3)
        time.sleep(1)