from rover.servo import Servo
from rover import constants
import time
import signal

pan_servo = Servo(constants.CAMERA_SERVOS['pan'])
tilt_servo = Servo(constants.CAMERA_SERVOS['tilt'])

if __name__ == '__main__':

    def signal_handler(sig, frame):
        pan_servo.set_angle(90)
        tilt_servo.set_angle(90)
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)

		
	
    num = 90
    while num>=0:
        num = int(input())
        pan_servo.set_angle(num)
