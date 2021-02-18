from DFRobot_BMX160 import BMX160
import time

# Just a tool for getting the sampling rate for the BMX sensor from the i2c port

bmx = BMX160(1)

while not bmx.begin():
    time.sleep(2)

def main():

    counter = 0
    cumtime = 0

    while True:
        currtime = time.time() * 1000; 
        data = bmx.get_all_data()
        cumtime += (time.time() * 1000) - currtime

        counter += 1

        if counter == 100:
            avetime = cumtime / counter
            counter = 0
            cumtime = 0
            print("Current average {}".format(avetime))



main()
    