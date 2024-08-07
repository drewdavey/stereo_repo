# Last updated: 2024-02-23
##################################
# This script is passed 5 arguments from run_burst.sh
# Args: (1) Cam0 path (2) Cam1 path (3) Log path (4) dt (5) duration
##################################

import sys
from picamera2 import Picamera2
import time
from datetime import datetime
from gpiozero import Button
from signal import pause
from threading import Timer
from functools import partial

i = 0  # Global index variable

def run(path0,path1,pathLog,dt,duration):
	button = Button(17)
	cam0 = Picamera2(0)
	cam1 = Picamera2(1)

	# Define camera configurations
	config0 = cam0.create_still_configuration()
	config1 = cam1.create_still_configuration()

	# Configuration settings
	config0['main']['size'] = (1440, 1080)  # Resolution for cam0
	config1['main']['size'] = (1440, 1080)  # Resolution for cam1
	config0['controls']['FrameDurationLimits'] = (33333, 33333)  # Frame rate (in microseconds) for cam0
	config1['controls']['FrameDurationLimits'] = (33333, 33333)  # Frame rate for cam1

	# Apply configurations
	cam0.configure(config0)
	cam1.configure(config1)

	cam0.start()
	cam1.start()

	meta0 = cam0.capture_metadata()
	meta1 = cam1.capture_metadata()

	# Write to log file
	outfile = open(pathLog, 'a')
	outfile.write('\n' + 'Start Time: ' + datetime.utcnow().strftime('%H%M%S%f')[:-3] + '\n')
	outfile.write('\n' + 'Cam0 Metadata:' + '\n')
	outfile.write(str(meta0) + '\n')
	outfile.write('\n' + 'Cam0 Config:' + '\n')
	outfile.write(str(config0) + '\n')
	outfile.write('' + '\n')
	outfile.write('Cam1 Metadata:' + '\n')
	outfile.write(str(meta1) + '\n')
	outfile.write('\n' + 'Cam1 Config:' + '\n')
	outfile.write(str(config1) + '\n')

	def capture(i):
		while button.is_pressed:
			timestamp = datetime.utcnow()
			tstr = timestamp.strftime('%H%M%S%f')[:-3]
			cam0.capture_file(f"{path0}0_{tstr}_{i+1:05}.jpg")
			cam1.capture_file(f"{path1}1_{tstr}_{i+1:05}.jpg")
			i += 1
			time.sleep(dt)

	def end_program():
		cam0.stop()
		cam1.stop()
		cam0.close()
		cam1.close()
		exit()

	# Set a timer to end the program after the specified duration
	Timer(duration, end_program).start()

	button.when_pressed = lambda: capture(i)
	
	outfile.write('\n' + 'Stop Time: ' + datetime.utcnow().strftime('%H%M%S%f')[:-3] + '\n')
	outfile.write('Done collecting images.' + '\n')
	outfile.close()
		

if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),int(sys.argv[5]))
