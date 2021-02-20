# Call function to read the value on the flex sensor
import spidev # To communicate with SPI devices
from numpy import interp    # To scale values
from time import sleep  # To add delay
import RPi.GPIO as GPIO # To use GPIO pins

def read_flex():
    # Start SPI connection
    spi = spidev.SpiDev() # Created an object
    spi.open(0,0)   

    # Initializing LED pin as OUTPUT pin
    led_pin = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)

    # Creating a PWM channel at 100Hz frequency
    pwm = GPIO.PWM(led_pin, 100)
    pwm.start(0)

    # Read MCP3008 data
    channel = 0
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    output = data # Reading from CH0
    output = interp(output, [0, 1023], [0, 100])
    pwm.ChangeDutyCycle(output)
    
    sleep(0.1)
    
    return output
