from DFRobot_BMX160 import BMX160
import time

# Just a tool for getting the sampling rate for the BMX sensor from the i2c port
# Average (lower bound) sampling rate determined to be ~480 samples/sec

bmx1 = BMX160(1, 0x69)

while not bmx1.begin():
    time.sleep(2)

def main():

    counter = 0
    cumtime = 0

    while True:
        currtime = time.time() * 1000; 
        data1 = bmx1.get_all_data()
        time.sleep(0.002)
        cumtime += (time.time() * 1000) - currtime

        counter += 1

        if counter == 100:
            avetime = cumtime / counter
            counter = 0
            cumtime = 0
            print("Current average {}".format(avetime))
        
        print("magn: x: {0:.2f} uT, y: {1:.2f} uT, z: {2:.2f} uT".format(data1[0],data1[1],data1[2]))
        print("gyro  x: {0:.2f} g, y: {1:.2f} g, z: {2:.2f} g".format(data1[3],data1[4],data1[5]))
        print("accel x: {0:.2f} m/s^2, y: {1:.2f} m/s^2, z: {2:.2f} m/s^2".format(data1[6],data1[7],data1[8]))
        print(" ")



main()
    