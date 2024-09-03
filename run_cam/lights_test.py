
from picamera2 import Picamera2
from gpiozero import Button, LED
from signal import pause
import subprocess
from settings import *
from datetime import datetime, timezone
from time import sleep


green = LED(12)

green.on()

process = subprocess.Popen(['python3', 'sub_lights.py'])

while not process.poll() is None:  # Check if standby.py is still running
    right_button = Button(18, hold_time=5) 
    left_button = Button(17, hold_time=5)
    if (right_button.is_held and left_button.is_held):
        green.close()
        right_button.close()
        left_button.close()
        exit()