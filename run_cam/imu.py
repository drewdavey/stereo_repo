
import sys
import time
import signal
from vnpy import *
from datetime import datetime, timezone
from utils import *

imu_headerLine = "Timestamp (UTC: HHMMSSsss), VN-200 Timestamp (UTC), Temperature (deg C), Pressure (Pa), Yaw (deg), Pitch (deg), Roll (deg), Accel_x, Accel_y, Accel_z, Gyro_x, Gyro_y, Gyro_z, Mag_x, Mag_y, Mag_z, GPS_LLA, INS_LLA\n"

# Connect to the VN-200 
# ez = EzAsyncData.connect('/dev/ttyUSB0', 115200)
# s = ez.sensor
s = VnSensor()
s.connect('/dev/ttyUSB0', 115200)

running = True

def imu_run(fname_imu,fname_log,imu_dt):
    global running
    imu = open(fname_imu, 'a')
    log = open(fname_log, 'a')
    tstr = datetime.now(timezone.utc).strftime('%H%M%S%f')[:-3]
    log.write(f"{tstr}:     IMU started.\n")
    imu.write(imu_headerLine)
    while running:
        tstr = datetime.now(timezone.utc).strftime('%H%M%S%f')[:-3]
        ypr = s.read_yaw_pitch_roll() # Read yaw, pitch, and roll values
        # gps = s.read_gps_solution_lla() # Read the GPS solution in LLA format
        # ins = s.read_ins_solution_lla() # Read the INS solution
        # imu_out = s.read_imu_measurements() # Read the IMU measurements
        # cd = ez.current_data # Read current data as CompositeData class from EzAsyncData
        # imu.write(f"{tstr}, {cd.time_utc}, {cd.temperature} or {imu_out.temp}, {cd.pressure} or {imu_out.pressure}, {ypr.x}, {ypr.y}, {ypr.z}, {imu_out.accel.x}, {imu_out.accel.y}, {imu_out.accel.z}, {imu_out.gyro.x}, {imu_out.gyro.y}, {imu_out.gyro.z}, {imu_out.mag.x}, {imu_out.mag.y}, {imu_out.mag.z}, ({gps.lla.x}, {gps.lla.y}, {gps.lla.z}), ({ins.position.x}, {ins.position.y}, {ins.position.z})" + '\n')
        imu.write(f"{tstr}, {ypr.x}, {ypr.y}, {ypr.z}" + '\n')
        time.sleep(imu_dt)
    tstr = datetime.now(timezone.utc).strftime('%H%M%S%f')[:-3]
    log.write(f"{tstr}:     IMU stopped.\n")
    log.close()
    imu.close()
    s.disconnect()
    sys.exit(0)

def imu_disconnect(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, imu_disconnect) # signal handling
signal.signal(signal.SIGINT, imu_disconnect)

if __name__ == '__main__':
    fdir, fname_log = setup_logging()             
    inputs = read_inputs_yaml(fname_log)
    imu_dt = inputs['imu_dt']
    imu_run(sys.argv[1],sys.argv[2], imu_dt)
