from read_sensor import BMXSensor

from DFRobot_BMX160 import BMX160

import imu_calc
from skinematics import imus
from skinematics import quat

import numpy as np

import time

initial_orientation = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])

# sensor = BMXSensor(R_init=initial_orientation)

# Choose analytical method to start, probably switch to madgwick

# sensor.q_type = "analytical"

bmx = BMX160(1)

NUM_SAMPLES = 10
DEBUG_MODE = 1

def get_imu_data():
    accel = np.zeros(shape=(NUM_SAMPLES,3))
    gyro = np.zeros(shape=(NUM_SAMPLES,3))
    magn = np.zeros(shape=(NUM_SAMPLES,3))

    cumtime = 0

    for i in range(NUM_SAMPLES):
        currtime = time.time() * 1000; 
        data = bmx.get_all_data()
        cumtime += (time.time() * 1000) - currtime

        accel[i] = [data[6], data[7], data[8]]
        gyro[i] = [data[3], data[4], data[5]]
        magn[i] = [data[0], data[1], data[2]]
    
    samp_period = cumtime / NUM_SAMPLES

    return accel, gyro, magn, samp_period

# position_computer = imus.Mahony(Sample.per#)

# orientation quaternions
q = np.zeros(shape=(NUM_SAMPLES,4)) # [quat.Quaternion([0., 0., 0., 0.]) for i in range(120)]

# position
pos = np.zeros(shape=(NUM_SAMPLES,3))

# velocity
vel = np.zeros(shape=(NUM_SAMPLES,3))

# Setup initial orientation, velocity and position

q[NUM_SAMPLES - 1] = np.array([1., 0., 0., 0.]) # quat.Quaternion(np.array([1.,0.,0.,0.]))

while 1:

    # Read IMU data and place into matrices to be analyzed in batches
    accel, gyro, magn, samp_period = get_imu_data()

    samp_freq = 1/(samp_period * (10**-3))

    # print(q[119])

    # Convert initial rotation quaternion into rotation matrix
    initial_rot = quat.convert(q[NUM_SAMPLES - 1], to='rotmat') # .export(to='rotmat')

    # Use analytical method to calculate position, orientation and velocity
    (q, pos, vel) = imu_calc.analytical(omega = gyro, 
                                        accMeasured = accel, 
                                        rate = samp_freq, 
                                        R_initialOrientation = initial_rot, 
                                        initialPosition = pos[NUM_SAMPLES - 1])

    if DEBUG_MODE == 1:
        print(gyro)
        print(samp_freq)
    
    print("Latest Position: {:.2f} {:.2f} {:.2f}, Orientation: {:.2f} {:.2f} {:.2f} {:.2f}".format(pos[NUM_SAMPLES - 1][0], pos[NUM_SAMPLES - 1][1], pos[NUM_SAMPLES - 1][2], q[NUM_SAMPLES - 1][0], q[NUM_SAMPLES - 1][1], q[NUM_SAMPLES - 1][2], q[NUM_SAMPLES - 1][3]))
