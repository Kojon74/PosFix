from DFRobot_BMX160 import BMX160

import imu_calc
from skinematics import imus
from skinematics import quat
import numpy as np

import time as time_lib
import asyncio

initial_orientation = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]])

# sensor = BMXSensor(R_init=initial_orientation)

# Choose analytical method to start, probably switch to madgwick

# sensor.q_type = "analytical"

NUM_SAMPLES = 10
DEBUG_MODE = 0

# Get the IMU data and return:
'''
accel = ndarray(NUM_SAMPLES,3) = Acceleration vector
gyro  = ndarray(NUM_SAMPLES,3) = Angulary velocity vector
magn  = ndarray(NUM_SAMPLES,3) = Magnetic field strength vector
rate  = float                  = Average rate
time  = ndarray(NUM_SAMPLES,1) = Time axis for integration, due to uneven sampling rate
'''
def get_imu_data(bmx: BMX160, prev_time):
    accel = np.zeros(shape=(NUM_SAMPLES,3))
    gyro = np.zeros(shape=(NUM_SAMPLES,3))
    magn = np.zeros(shape=(NUM_SAMPLES,3))

    time_vec = np.zeros(NUM_SAMPLES)

    cumtime = 0

    start_time = time_lib.time() 
    new_time = (start_time - prev_time) * 1000

    # print("Time between runs {} ms".format(new_time))

    for i in range(NUM_SAMPLES):
        currtime = time_lib.time()
        data = bmx.get_all_data()
        finishtime = (time_lib.time()) - currtime
        cumtime += finishtime

        accel[i] = [data[6], data[7], data[8]]
        gyro[i] = [data[3], data[4], data[5]]
        magn[i] = [data[0], data[1], data[2]]
        
        time_vec[i] = cumtime
    
    samp_period = cumtime / NUM_SAMPLES

    return accel, gyro, magn, samp_period, time_vec, start_time

# position_computer = imus.Mahony(Sample.per#)

async def data_loop(bmx: BMX160, q, pos, vel, prev_time):
    # Read IMU data and place into matrices to be analyzed in batches
    accel, gyro, magn, samp_period, time, prev_time1 = get_imu_data(bmx, prev_time)

    samp_freq = 1/(samp_period)

    # print(q[119])

    # Convert initial rotation quaternion into rotation matrix
    initial_rot = quat.convert(q[NUM_SAMPLES - 1], to='rotmat') # .export(to='rotmat')

    # print(q[NUM_SAMPLES - 1])

    # # Use analytical method to calculate position, orientation and velocity
    # (q1, pos1, vel1) = imu_calc.calc_orientation_position(omega = gyro, 
    #                                     accMeasured = accel, 
    #                                     rate = samp_freq, 
    #                                     initialOrientation = initial_rot, 
    #                                     initialPosition = pos[NUM_SAMPLES - 1],
    #                                     initialVelocity= vel[NUM_SAMPLES - 1],
    #                                     timeVector=time)

    # Use Kalmans method to calculate orientation, and position

    q1 = imu_calc.kalman(rate=samp_freq,
                        acc=accel,
                        omega=gyro,
                        mag=magn,
                        initialPosition=pos[NUM_SAMPLES - 1],
                        initialVelocity=vel[NUM_SAMPLES - 1],
                        timeVector=time)

    return q1, prev_time1

async def run_data_acquisition(bmxs, f):
    # orientation quaternions
    q = [np.zeros(shape=(NUM_SAMPLES,4)) for i in range(len(bmxs))] # [quat.Quaternion([0., 0., 0., 0.]) for i in range(120)]

    # position
    pos = [np.zeros(shape=(NUM_SAMPLES,3)) for i in range(len(bmxs))]

    # velocity
    vel = [np.zeros(shape=(NUM_SAMPLES,3)) for i in range(len(bmxs))]

    # Setup initial orientation, velocity and position

    for qi in q:
        qi[NUM_SAMPLES - 1] = np.array([1., 0., 0., 0.]) # quat.Quaternion(np.array([1.,0.,0.,0.]))

    # Wait for IMU  to init

    for bmx in bmxs:
        while not bmx.begin():
            print("Waiting for IMU...")
            time_lib.sleep(1)

    last_time = [0] * len(bmxs)

    current_inc = 0

    while 1:
        # Create tasks

        num_tasks = 0
        tasks = [None] * len(bmxs)

        for bmx in bmxs:
            tasks[num_tasks] = asyncio.create_task(
                data_loop(bmx, q[num_tasks], pos[num_tasks], vel[num_tasks], last_time[num_tasks])
            )

            num_tasks += 1

        for i in range(len(tasks)):
            (q[i], last_time[i]) = await tasks[i]

        if DEBUG_MODE == 1:
            print("q")
            print(q)
            # print("pos")
            # print(pos)
            print(samp_freq)
        
        current_inc += 1
        
        if (current_inc % 10 == 0):
            f.seek(0)
            for i in range(len(q)):
                f.write("{},{},{},{}\n".format(q[i][NUM_SAMPLES - 1][0], q[i][NUM_SAMPLES - 1][1], q[i][NUM_SAMPLES - 1][2], q[i][NUM_SAMPLES - 1][3]))
                # await print_output(q[i], pos[i], vel[i], i)
            f.flush()

async def print_output(q, pos, vel, sens):
    # print("Sensor: {} Latest Position: {:.2f} {:.2f} {:.2f}, V: {:.2f} {:.2f} {:.2f},  Orientation: {:.2f} {:.2f} {:.2f} {:.2f}".format(sens, pos[NUM_SAMPLES - 1][0], pos[NUM_SAMPLES - 1][1], pos[NUM_SAMPLES - 1][2], vel[NUM_SAMPLES - 1][0], vel[NUM_SAMPLES - 1][1], vel[NUM_SAMPLES - 1][2], q[NUM_SAMPLES - 1][0], q[NUM_SAMPLES - 1][1], q[NUM_SAMPLES - 1][2], q[NUM_SAMPLES - 1][3]))
    print("Sensor: {} Orientation: {:.2f} {:.2f} {:.2f} {:.2f}".format(sens, q[NUM_SAMPLES - 1][0], q[NUM_SAMPLES - 1][1], q[NUM_SAMPLES - 1][2], q[NUM_SAMPLES - 1][3]))

def begin_recording():
    bmx1 = BMX160(1, 0x68)
    bmx2 = BMX160(1, 0x69)

    bmx3 = BMX160(4, 0x68)
    bmx4 = BMX160(4, 0x69)

    f = open("../sensordata.log", 'w')

    asyncio.run(
        run_data_acquisition([bmx1, bmx2], f)
    ) 

    f.close()

def main():
    begin_recording()

main()