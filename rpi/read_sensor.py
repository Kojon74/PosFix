
import numpy as np
import pandas as pd
import abc

import os
import sys

from imus import IMU_Base
from DFRobot_BMX160 import BMX160

sensor = BMX160(1)

class BMXSensor(IMU_Base):
    # Get Data function

    def get_data(self, in_file=None, in_data=None):
        #get data from sensor here....

        data = bmx.get_all_data()
        
        rate = 48000

        out_data = {'rate' : rate,
                    'acc' : {data[6], data[7], data[8]},
                    'omega' : {data[3], data[4], data[5]},
                    'mag': {data[0], data[1], data[2]}
                    }

        self._set_data(out_data)
