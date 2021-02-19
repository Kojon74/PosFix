
import numpy as np
import pandas as pd
import abc

import os
import sys

from skinematics.imus import IMU_Base
from DFRobot_BMX160 import BMX160

sensor = BMX160(1)

class BMXSensor(IMU_Base):
    # Get Data function

    def get_data(self, in_file=None, in_data=None):
        #get data from sensor here....

        data = bmx.get_all_data()
        
        accel = numpy.zeros(shape=(120,3))
        gyro = numpy.zeros(shape=(120,3))
        magn = numpy.zeros(shape=(120,3))

        cumtime = 0

        for i in range(120):
            currtime = time.time() * 1000; 
            data = bmx.get_all_data()
            cumtime += (time.time() * 1000) - currtime

            accel[i] = [data[6], data[7], data[8]]
            gyro[i] = [data[3], data[4], data[5]]
            magn[i] = [data[0], data[1], data[2]]
        
        samp_period = cumtime / 120

        out_data = {'rate' : rate,
                    'acc' : accel,
                    'omega' : gyro,
                    'mag': magn
                    }

        self._set_data(out_data)
