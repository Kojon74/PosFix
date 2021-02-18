
from skinematics.sensors.manual import MyOwnSensor
from read_sensors import BMXSensor

initial_orientation = np.array([[1,0,0], [0,0,-1], [0,1,0]])

sensor = BMXSensor(R_init=initial_orientation)

# Choose analytical method to start, probably switch to madgwick

sensor.q_type = "analytical"

while 1:
    print(sensor.)
