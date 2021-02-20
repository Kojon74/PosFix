# function to read log file orientation data
def read_orientation():
    file = open('../sensordata.log','r')
    lines = file.read().splitlines()
    file.close()
    
    imu_1 = lines[0].split(',')
    imu_2 = lines[1].split(',')
    imu_3 = lines[2].split(',')
    imu_4 = lines[3].split(',')
    
    sensor_output = [imu_1,imu_2,imu_3, imu_4]
    return sensor_output