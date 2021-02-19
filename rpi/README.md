# PosFix - Raspberry PI Code
Team MakeBooty's MakeUofT 2021 project. This folder contains all the code that will run on the raspberry pi

## What's in here
1. getpos.py - Reads the data from the IMU's and returns orientation, position, and velocity relative to the earth
2. test_baudrate.py - Helper file to get the speed of the I2C port
3. imu_calc.py - Slightly modified function from the scipy-kinematics library, to add changes that will allow it to work for real time computation