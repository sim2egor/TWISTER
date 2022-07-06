# Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=242928\.
#
# Software to drive 4 wire stepper motor using a TB6600 Driver
# PRi - RPi 3B
#
# Route 3.3 VDC to the controller "+" input for each: ENA, PUL, and DIR
#
# Connect GPIO pins as shown below) to the "-" input for each: ENA, PUL, and DIR
#
#
from itertools import cycle
from time import sleep
import RPi.GPIO as GPIO
#
class STMotor:
    cyclecount=0
    cycles = 0
    def __init__(self) -> None:
        # self.PUL = 17  # Stepper Drive Pulses
        # self.DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).

        self.PUL = 5  # Stepper Drive Pulses
        self.DIR = 6  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).

        self.ENA = 16  # Controller Enable Bit (High to Enable / LOW to Disable).
        # DIRI = 14  # Status Indicator LED - Direction
        # ENAI = 15  # Status indicator LED - Controller Enable
        #
        # NOTE: Leave DIR and ENA disconnected, and the controller WILL drive the motor in Default direction if PUL is applied.
        # 
        GPIO.setmode(GPIO.BCM)
        # GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only. 
        #
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        # GPIO.setup(DIRI, GPIO.OUT)
        # GPIO.setup(ENAI, GPIO.OUT)
        #
        print('PUL = GPIO 5 - RPi 3B-Pin #11')
        print('DIR = GPIO 6 - RPi 3B-Pin #13')
        print('ENA = GPIO 16 - RPi 3B-Pin #15')
        # print('ENAI = GPIO 14 - RPi 3B-Pin #8')
        # print('DIRI = GPIO 15 - RPi 3B-Pin #10')

        #
        print('Initialization Completed')
        #
            # Could have usesd only one DURATION constant but chose two. This gives play options.
        self.durationFwd = 4000 # This is the duration of the motor spinning. used for forward direction
        self.durationBwd = 4000 # This is the duration of the motor spinning. used for reverse direction
        print('Duration Fwd set to ' + str(self.durationFwd))
        print('Duration Bwd set to ' + str(self.durationBwd))
        # plus 100-156 mikrosek
        self.delay = 0.00001*2 # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
        print('Speed set to ' + str(self.delay))
        #
        self.cycles = 1000 # This is the number of cycles to be run once program is started.
        self.cyclecount = 0 # This is the iteration of cycles to be run once program is started.
        print('number of Cycles to Run set to ' + str(self.cycles))
        #
        #
    def forward(self):
        GPIO.output(self.ENA, GPIO.HIGH)
        # GPIO.output(ENAI, GPIO.HIGH)
        print('ENA set to HIGH - Controller Enabled')
        #
        sleep(.5) # pause due to a possible change direction
        GPIO.output(self.DIR, GPIO.LOW)
        # GPIO.output(DIRI, GPIO.LOW)
        print('DIR set to LOW - Moving Forward at ' + str(self.delay))
        print('Controller PUL being driven.')
        for x in range(self.durationFwd): 
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.delay)
        GPIO.output(self.ENA, GPIO.LOW)
        # GPIO.output(ENAI, GPIO.LOW)
        print('ENA set to LOW - Controller Disabled')
        sleep(.5) # pause for possible change direction
        return
    #
    #
    def reverse(self):
        GPIO.output(self.ENA, GPIO.HIGH)
        # GPIO.output(ENAI, GPIO.HIGH)
        print('ENA set to HIGH - Controller Enabled')
        #
        sleep(.5) # pause due to a possible change direction
        GPIO.output(self.DIR, GPIO.HIGH)
        # GPIO.output(DIRI, GPIO.HIGH)
        print('DIR set to HIGH - Moving Backward at ' + str(self.delay))
        print('Controller PUL being driven.')
        #
        for y in range(self.durationBwd):
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.delay)
        GPIO.output(self.ENA, GPIO.LOW)
        # GPIO.output(ENAI, GPIO.LOW)
        print('ENA set to LOW - Controller Disabled')
        sleep(.5) # pause for possible change direction
        return
    def goto_l(self,NumStep,num):
        GPIO.output(self.ENA, GPIO.HIGH)
        # GPIO.output(ENAI, GPIO.HIGH)
        print('ENA set to HIGH - Controller Enabled')
        #
        sleep(.5) # pause due to a possible change direction
        GPIO.output(self.DIR, GPIO.LOW)
        # GPIO.output(DIRI, GPIO.LOW)
        print('DIR set to LOW - Moving Forward at ' + str(self.delay))
        print('Controller PUL being driven.')
        for x in range(NumStep):
            num.value = num.value -1 
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.delay)
        GPIO.output(self.ENA, GPIO.LOW)
        # GPIO.output(ENAI, GPIO.LOW)
        print('ENA set to LOW - Controller Disabled')
        sleep(.5) # pause for possible change direction
        return
    def goto_r(self,NumStep,num):
        GPIO.output(self.ENA, GPIO.HIGH)
        # GPIO.output(ENAI, GPIO.HIGH)
        print('ENA set to HIGH - Controller Enabled')
        #
        sleep(.5) # pause due to a possible change direction
        GPIO.output(self.DIR, GPIO.HIGH)
        # GPIO.output(DIRI, GPIO.HIGH)
        print('DIR set to HIGH - Moving Backward at ' + str(self.delay))
        print('Controller PUL being driven.')
        #
        for y in range(NumStep):
            num.value =num.value+1
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(self.delay)
        GPIO.output(self.ENA, GPIO.LOW)
        # GPIO.output(ENAI, GPIO.LOW)
        print('ENA set to LOW - Controller Disabled')
        sleep(.5) # pause for possible change direction
        return

if __name__ == '__main__':
    class number:
        value=0

    d1=STMotor()
    cycles=d1.cycles
    num=number()
    num.value=1
    while d1.cyclecount < d1.cycles:
        #d1.forward()
        #d1.reverse()
        d1.goto_r(2*40000,num)
        sleep(2)
        d1.goto_l(2*40000,num)
        sleep(2)
        d1.cyclecount = (d1.cyclecount + 1)
        print('Number of cycles completed: ' + str(d1.cyclecount))
        print('Number of cycles remaining: ' + str(d1.cycles - d1.cyclecount))
    #
    GPIO.cleanup()
    print('Cycling Completed')
#
