from read_sensor import BMXSensor

from DFRobot_BMX160 import BMX160

from skinematics import imus
from skinematics import quat

import numpy as np

import time

initial_orientation = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])

# sensor = BMXSensor(R_init=initial_orientation)

# Choose analytical method to start, probably switch to madgwick

# sensor.q_type = "analytical"

bmx = BMX160(1)

def get_imu_data():
    accel = np.zeros(shape=(120,3))
    gyro = np.zeros(shape=(120,3))
    magn = np.zeros(shape=(120,3))

    cumtime = 0

    for i in range(120):
        currtime = time.time() * 1000; 
        data = bmx.get_all_data()
        cumtime += (time.time() * 1000) - currtime

        accel[i] = [data[6], data[7], data[8]]
        gyro[i] = [data[3], data[4], data[5]]
        magn[i] = [data[0], data[1], data[2]]
    
    samp_period = cumtime / 120

    return accel, gyro, magn, samp_period

# position_computer = imus.Mahony(Sample.per#)

# orientation quaternions
q = [quat.Quaternion([0., 0., 0., 0.]) for i in range(120)]

# position
pos = np.zeros(shape=(120,3))

# velocity
vel = np.zeros(shape=(120,3))

# Setup initial orientation, velocity and position

q[119] = quat.Quaternion(np.array([0.,0.,0.,1.]))

pos[119] = np.array([0., 0., 0.])

while 1:

    accel, gyro, magn, samp_period = get_imu_data()

    samp_freq = 1/(samp_period * (10**-3))

    print(q[119])
    initial_rot = quat.convert(q[119], to='rotmat').reshape(3,3)

    # Use analytical method to calculate position, orientation and velocity
    (q, pos, vel) = imus.analytical(omega = gyro, 
                                        accMeasured = accel, 
                                        rate = samp_freq, 
                                        R_initialOrientation = initial_rot, 
                                        initialPosition = pos[119])
    
    print("Latest Position: {} {} {}, Orientation: {} {} {} {}".format(pos[119][0], pos[119][1], pos[119][2], q[119][0], q[119][1], q[119][2], q[119][3]))

