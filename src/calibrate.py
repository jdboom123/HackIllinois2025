from rover.servo import Servo
from rover import constants
from rover.sonar import Sonar
from rover.sonar_led import SonarLEDS
from rover.camera import Camera
from rover.drivetrain import Drivetrain

import time
import signal
import random
import cv2
import matplotlib.pyplot as plt
import numpy as np

pan_servo = Servo(constants.CAMERA_SERVOS['pan'])
tilt_servo = Servo(constants.CAMERA_SERVOS['tilt'])
sonar = Sonar()
sonar_leds = SonarLEDS()
camera = Camera()
drivetrain = Drivetrain()

SCAN_PAN_MIN, SCAN_PAN_MAX, SCAN_PAN_DELTA = 35, 140, 20
SCAN_TILT_MIN, SCAN_TILT_MAX, SCAN_TILT_DELTA = 80, 135, 12

SPEED = 50


if __name__ == '__main__':
	def signal_handler(sig, frame):
		drivetrain.set_motion(speed=0, heading=90)
		exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	
	
	while True:
		sec = float(input())
		
		# Turn amount of degrees
		drivetrain.set_motion(angular_speed=50)
		time.sleep(sec)
		drivetrain.set_motion(angular_speed=0)
		
		
		sec = float(input())
		drivetrain.set_motion(speed=50)
		time.sleep(sec)
		drivetrain.set_motion(speed=0)

		
		
	
