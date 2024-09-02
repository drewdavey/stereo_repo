# Last updated: 2024-04-10
##################################
# This script is passed 5 arguments from run_numFrames.sh
# Args: (1) Cam0 path (2) Cam1 path (3) Log path (4) Number of frames (5) dt
##################################

import os
import time
import yaml
import subprocess
from vnpy import *
from datetime import datetime, timezone

def setup_logging():
    fdir = f"../../DATA/{datetime.now(timezone.utc).strftime('%Y%m%d')}/"
    if not os.path.exists(fdir):
        os.makedirs(fdir)
    fname_log = os.path.join(fdir, f"{datetime.now(timezone.utc).strftime('%Y%m%d')}_LOG.txt")
    if not os.path.exists(fname_log) or os.stat(fname_log).st_size == 0:
        header_block = """
########################################################################################################################
#                                                                                                                      #
#                               *****      *******      ****      *    *     *******                                   #
#                              *              *        *    *     *  *       *                                         #
#                               *****         *        *    *     * *        ****                                      #
#                                    *        *        *    *     *  *       *                                         #    
#                               *****         *         ****      *    *     *******                                   #   
#                                                                                                                      #
########################################################################################################################
                                # STereo camera system for Overturning wave KinEmatics #
                                #   Developed at Scripps Institution of Oceanography   #
                                #             Date: {}                #
                                ########################################################
""".format(datetime.now(timezone.utc).strftime('%Y-%m-%d-%H-%M-%S'))
        with open(fname_log, 'w') as log:
            log.write(header_block)
            log.write("\n\n\n")
    return fdir, fname_log

def read_inputs_yaml(fname_log):
    inputs_path = '../inputs.yaml'
    with open(fname_log, 'a') as log:
        try:
            with open(inputs_path, 'r') as file:
                inputs = yaml.safe_load(file)
            return inputs
        except FileNotFoundError:
            log.write(f"Error: The file {inputs_path} was not found.")
            return None
        except yaml.YAMLError as exc:
            log.write(f"Error parsing YAML file: {exc}")
            return None
    
def sync_clock_and_imu(fname_log):
    ez = EzAsyncData.connect('/dev/ttyUSB0', 115200) # Create sensor object and connect to the VN-200 
    s = ez.sensor                                    # at the baud rate of 115200 (115,200 bytes/s) 
    # s = VnSensor()
    # s.connect('/dev/ttyUSB0', 115200)
    with open(fname_log, 'a') as log:
        model_num = s.read_model_number()
        serial_num = s.read_serial_number()
        tstr = datetime.now(timezone.utc).strftime('%H%M%S%f')[:-3]
        log.write(f"{tstr}:     Connected to VN-200: Model {model_num}, Serial: {serial_num}\n")
        log.write(f"{tstr}:     Waiting for VN-200 to acquire GPS fix...\n")
        i = 0 
        while ez.current_data.position_uncertainty_estimated > 10:
            # num_sats = ez.current_data.num_sats
            # log.write(f"Number of satellites: {num_sats}\n")
            time.sleep(1)
            i += 1
            if i > 60:
                log.write(f"{tstr}:     VN-200 could not acquire GPS fix. Exiting.\n")
                break
        tstr = datetime.now(timezone.utc).strftime('%H%M%S%f')[:-3]
        if ez.current_data.has_any_position:
            pos = ez.current_data.any_position
            log.write(f"{tstr}:     Position: ({pos})\n")
            posun = ez.current_data.any_position_uncertainty
            log.write(f"{tstr}:     Position uncertainty: ({posun.x}, {posun.y}, {posun.z})\n")
            posunes = ez.current_data.position_uncertainty_estimated
            log.write(f"{tstr}:     Position uncertainty estimated: {posunes}\n")
        if ez.current_data.has_time_gps:
            vn_time = ez.current_data.time_utc
            log.write(f"{tstr}:     Time from VN-200: {vn_time}\n")
        if ez.current_data.has_num_sats:
            num_sats = ez.current_data.num_sats
            log.write(f"{tstr}:     Number of satellites: {num_sats}\n")
        gps_sol = s.read_gps_solution_lla()
        log.write(f"{tstr}:     GPS Solution (LLA): ({gps_sol.lla.x}, {gps_sol.lla.y}, {gps_sol.lla.z})\n")
    log.close()
    s.disconnect()

def enter_standby(fdir, fname_log, dt, num_frames):
    tstr = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    with open(fname_log, 'a') as log:
        log.write(f"Startup complete - created log for {tstr}.\n\n")
    subprocess.Popen(['python3', 'standby.py', fdir, fname_log, str(dt), str(num_frames)])

def startup():
    fdir, fname_log = setup_logging()               # Setup logging
    inputs = read_inputs_yaml(fname_log)            # Read inputs from inputs.yaml
    num_frames = inputs['num_frames']
    dt = inputs['dt']
    calib_on_boot = inputs['calib_on_boot']
    launch_standby = inputs['launch_standby']
    mode = inputs['shooting_mode']                   # pass to settings.py
    sync_clock_and_imu(fname_log)                    # Connect to VecNav and sync clock
    if calib_on_boot:
        subprocess.Popen(['python3', 'calib.py', fdir, fname_log, num_frames, dt]) # path0,path1,fname_log,calib_frames,dt
    if launch_standby:
        enter_standby(fdir, fname_log, dt, num_frames)    # Enter standby mode

if __name__ == "__main__":
    startup()