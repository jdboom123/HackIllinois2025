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
import matplotlib
matplotlib.use('TkAgg')  # or 'Agg' if you dont need a window

import matplotlib.pyplot as plt
import numpy as np


pan_servo = Servo(constants.CAMERA_SERVOS['pan'])
tilt_servo = Servo(constants.CAMERA_SERVOS['tilt'])
sonar = Sonar()
sonar_leds = SonarLEDS()
camera = Camera()
drivetrain = Drivetrain()

SCAN_PAN_MIN, SCAN_PAN_MAX, SCAN_PAN_DELTA = 25, 150, 20
SCAN_TILT_MIN, SCAN_TILT_MAX, SCAN_TILT_DELTA = 80, 135, 12

SPEED = 50
SEC_PER_90_DEG = 0.7
IN_PER_SEC = 11.5

# Color Gradient from Red to Green + White
COLORS = [0xd91a1a, 0xd46a19, 0xd49c19, 0xd4b519, 0x42d419, 0x19d4c7, 0xFFFFFF]	

# Distance Constants
DIST_PER_COLOR = 160 	# The amount of units between the distinct "zones"
MAX_FLOOR_DIST = 200  	# The distance at which we see a cliff
DIST_MARGIN = 15	# The margin in which two measurments are considered the "same"
TOO_CLOSE_DIST = 300 	


def detect_green_ball(image: np.ndarray):
    """
    Detects a green ball in the input image, draws a rectangle around it,
    and returns the modified image along with the center coordinates.
    
    :param image: Input image in BGR format (numpy array)
    :return: (modified_image, (center_x, center_y)) or (image, None) if no ball is found
    """

    # Define lower and upper bounds for green color in HSV
    LOWER_GREEN = np.array([40, 40, 40])   # Adjust based on lighting conditions
    UPPER_GREEN = np.array([80, 255, 255]) # Adjust for best detection

    # Convert BGR image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create a binary mask where green colors are in range
    mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assumed to be the green ball)
        largest_contour = max(contours, key=cv2.contourArea)

        # Get bounding rectangle around the green object
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        if w * h < 3000:
            return image, None, None

        # Compute center of the rectangle
        center_x, center_y = x + w // 2, y + h // 2

        # Draw the rectangle and center point on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

        # Display center coordinates
        cv2.putText(image, f"({center_x}, {center_y}) Area: {w*h}", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return image, (center_x, center_y), (w, h)
    
    return image, None, None # No green ball found

# Example usage with a live camera feed
if __name__ == "__main__":
	def signal_handler(sig, frame):
		drivetrain.set_motion(speed=0)
		exit(0)
	signal.signal(signal.SIGINT, signal_handler)
	
	
	plt.ion()
	fig, ax = plt.subplots()
		
	
	# Waiting for Ball
	while True:
		camera.capture()
		frame = camera.image_array
		frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)

		# Process frame
		processed_frame, center, dims = detect_green_ball(frame)
		if center != None:
			break
		time.sleep(0.1)
		
		
		# Show the processed frame
		ax.clear()
		ax.imshow(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
		plt.draw()  # Force Matplotlib to update
		plt.pause(0.01)  # Pause for a short moment to allow updates


	# Following Ball
	while True:
		camera.capture()
		frame = camera.image_array
		frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)

		# Process frame
		processed_frame, center, ball_dims = detect_green_ball(frame)
		if center is None:
			drivetrain.set_motion(speed=0)
			continue
		time.sleep(0.1)
		
		# Ball distances from center
		img_w, img_h, _ = frame.shape
		delta_x, delta_y = img_w//2-center[0], img_h//2-center[1]
		print(delta_x)
		# Turn to get ball in the middle
		CENTER_DEVIATION = 80
		ball_in_center = False
		if (delta_x > CENTER_DEVIATION):
			drivetrain.set_motion(angular_speed=-SPEED)
			#drivetrain.set_motion(speed=SPEED, heading=0)
		elif (delta_x < -CENTER_DEVIATION):
			drivetrain.set_motion(angular_speed=SPEED)
			#drivetrain.set_motion(speed=SPEED, heading=180)
		else:
			ball_in_center = True
			drivetrain.set_motion(angular_speed=0)
			
		# Move forward towards the ball
		GOAL_AREA = 21000
		if ball_in_center:
			if ball_dims[0] * ball_dims[1] < GOAL_AREA:	
				drivetrain.set_motion(speed=SPEED)
			elif ball_dims[0] * ball_dims[1] >= GOAL_AREA:
				drivetrain.set_motion(speed=0)
				break
			else:
				drivetrain.set_motion(speed=0)
				
		
		# Show the processed frame
		ax.clear()
		ax.imshow(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
		plt.draw()  # Force Matplotlib to update
		plt.pause(0.01)  # Pause for a short moment to allow updates
	
	print("Achieved goal")
	time.sleep(10)
	
	drivetrain.set_motion(speed=0)
