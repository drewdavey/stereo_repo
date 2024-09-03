# Last updated: 2024-04-10
##################################
# This file contains functions defining the camera settings for various shooting modes
##################################
from utils import *
from picamera2 import Picamera2
from libcamera import ColorSpace, Transform

def auto():
    cam = Picamera2()
    config = cam.create_still_configuration()
    config['main']['size'] = (1440, 1080)
    cam.close()
    return config

def standard():
    cam = Picamera2()
    config = cam.create_still_configuration()
    config['main']['size'] = (1440, 1080)
    config['main']['format'] = 'RGB888'
    config['controls']['FrameDurationLimits'] = (33333, 33333)  
    config['controls']['ExposureTime'] = 5000 
    cam.close()
    return config

def bright():
    cam = Picamera2()
    config = cam.create_still_configuration()
    config['main']['size'] = (1440, 1080)
    config['main']['format'] = 'RGB888'
    config['controls']['FrameDurationLimits'] = (33333, 33333)  
    config['controls']['ExposureTime'] = 2000
    cam.close()
    return config

def dark():
    cam = Picamera2()
    config = cam.create_still_configuration()
    config['main']['size'] = (1440, 1080)
    config['main']['format'] = 'RGB888'
    config['controls']['FrameDurationLimits'] = (33333, 33333)  
    config['controls']['ExposureTime'] = 100000 
    cam.close()
    return config

def fast():
    cam = Picamera2()
    config = cam.create_still_configuration()
    config['main']['size'] = (1440, 1080)
    config['main']['format'] = 'RGB888'
    config['controls']['FrameDurationLimits'] = (2000, 2000)  
    config['controls']['ExposureTime'] = 1000
    cam.close()
    return config

def max():
    cam = Picamera2()
    config = cam.create_still_configuration()
    config['main']['size'] = (1440, 1080)
    config['main']['format'] = 'RGB888'
    config['controls']['FrameDurationLimits'] = (100, 100)  
    config['controls']['ExposureTime'] = 50
    cam.close()
    return config

def get_config():
    fdir, fname = setup_logging()
    inputs = read_inputs_yaml(fname)
    mode = inputs['shooting_mode']
    if mode == 'auto':
        return auto()
    elif mode == 'standard':
        return standard()
    elif mode == 'bright':
        return bright()
    elif mode == 'dark':
        return dark()
    elif mode == 'fast':
        return fast()
    elif mode == 'max':
        return max()
    else:
        raise ValueError(f"Invalid mode: {mode}")


