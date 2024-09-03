
from gpiozero import Button, LED
import subprocess
import time
from subprocess import Popen
from signal import SIGINT



right_button = Button(18, hold_time=3)  
left_button = Button(17, hold_time=3)
# right_button.close()
# left_button.close()
# right_button = Button(18, hold_time=3)  
# left_button = Button(17, hold_time=3)

# green = LED(12)

LED(12).on()

while True:
    if (right_button.is_held and left_button.is_held): 
        right_button.close()
        left_button.close()
        LED(12).close() 
        time.sleep(1)
        process = subprocess.Popen(['python3', 'sub_lights.py'])
        process.wait()
        right_button = Button(18, hold_time=3)  
        left_button = Button(17, hold_time=3)
        time.sleep(1)


# if (right_button.is_held and left_button.is_held): 
#     right_button.close()
#     left_button.close() 
#     process = subprocess.Popen(['python3', 'sub_lights.py'])
#     process.wait()
#     right_button = Button(18, hold_time=3)  
#     left_button = Button(17, hold_time=3)
#     sleep(1)
