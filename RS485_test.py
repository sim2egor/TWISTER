from itertools import cycle
from time import sleep
import RPi.GPIO as GPIO
import sys
import pr6100Rs485 as PR

def main():
    print("Start left")
    try:
        PR.Start_(1,1,0)
        # PR.Start_(200,2,1)
        pass
    except Exception as e:
        print(e)
        PR.Stop_(1)
    sleep(60)
    print("stop left")
    PR.Stop_(1)
    sleep(1)
    print("Start right")
    try:
        PR.Start_(1,1,1)
        # PR.Start_(200,2,1)
        pass
    except Exception as e:
        print(e)
        PR.Stop_(1)
    sleep(60)
    print("Stop right")
    PR.Stop_(1)

	# try:
    #     # PR.Start_(frqUP,1,0)
    #     # PR.Start_(frqDown,2,FWDtmp)
    # except Exception as e:
	# 	print(e)

if __name__ == '__main__':
    main()
