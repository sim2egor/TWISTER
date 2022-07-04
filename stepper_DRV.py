from time import sleep
import RPi.GPIO as GPIO
import asyncio
#
# DIRI = 14  # Status Indicator LED - Direction
# ENAI = 15  # Status indicator LED - Controller Enable
#
# NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.
# 
class stepper_DRV:

    def __new__(cls, *args, **kwargs):
        print("Hello from __new__")
        return super().__new__(cls)


    def __init__(self) -> None:
        self.PUL = 5  # Stepper Drive Pulses
        self.DIR = 6  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
        self.ENA = 16  # Controller Enable Bit (High to Enable / LOW to Disable).
        self.delay = 0.0000001 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
        print("Hello from __init__")
        GPIO.setmode(GPIO.BCM)
        # GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
        #
        GPIO.setup(PUL, GPIO.OUT)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(ENA, GPIO.OUT)
        # GPIO.setup(DIRI, GPIO.OUT)
        # GPIO.setup(ENAI, GPIO.OUT)
        #
        print('PUL = GPIO 5 - RPi 3B-Pin #11')
        print('DIR = GPIO 6 - RPi 3B-Pin #13')
        print('ENA = GPIO 16 - RPi 3B-Pin #15')

    def rot_l():

        


def main():
    d1=stepper_DRV()

if __name__ == '__main__':
    main()
