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

def set_leds(color):
	# Set both LED colors the same
	sonar_leds.left.setPixelColor(color)
	sonar_leds.right.setPixelColor(color)

def read_sonar():
	dist = sonar.get_distance()
	
	# Set LED color depending on distance
	if dist < DIST_PER_COLOR:
		set_leds(COLORS[0])
	elif dist < DIST_PER_COLOR*2:
		set_leds(COLORS[1])
	elif dist < DIST_PER_COLOR*3:
		set_leds(COLORS[2])
	elif dist < DIST_PER_COLOR*4:
		set_leds(COLORS[3])
	elif dist < DIST_PER_COLOR*5:
		set_leds(COLORS[4])
	elif dist == 5000:
		set_leds(COLORS[6])
	else:
		set_leds(COLORS[5])
		
	return dist

def scan_strip(deg):
	# Set the tilt angle
	tilt_servo.set_angle(deg)
	time.sleep(0.6)
    
    # Scan across a horizontal line
	depth_data = []
	for i in range(SCAN_PAN_MIN, SCAN_PAN_MAX, SCAN_PAN_DELTA):
		pan_servo.set_angle(i)
		time.sleep(0.6)
		
		depth_data.append(read_sonar())
		time.sleep(0.3)
		
	# Return data
	return depth_data
		
def full_scan():
	# Perform a multiple horizontal scans at different tilts
	full_data = []
	for deg in range(SCAN_TILT_MIN, SCAN_TILT_MAX, SCAN_TILT_DELTA):
		full_data.append(scan_strip(deg))
		time.sleep(1)
	
	return full_data

def show_camera_frame(sonar_data, fig, ax):	
	camera.capture()
	frame = camera.image_array
	frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)
                
	# Get frame dimensions
	h, w, _ = frame.shape
	data_h, data_w = len(sonar_data), len(sonar_data[0])
	grid_h, grid_w = h // data_h, w // data_w

	for i in range(data_h):
		for j in range(data_w):
			x1, y1 = j * grid_w, i * grid_h  # Top-left corner
			x2, y2 = (j + 1) * grid_w, (i + 1) * grid_h  # Bottom-right corner
	
			# Select color based on distance and convert to BGR
			sonar_dist = sonar_data[i][j]
			color_idx = 6 if sonar_dist == 5000 else min(5, sonar_dist//DIST_PER_COLOR)
			color = COLORS[color_idx]  
			
			def hex_to_bgr(hex_color):
					"""Convert 0xRRGGBB to (B, G, R) format for OpenCV."""
					b = (hex_color & 0xFF)
					g = (hex_color >> 8) & 0xFF
					r = (hex_color >> 16) & 0xFF
					return (b, g, r)
			scolor = hex_to_bgr(color)
			
			# Add a highlighted rectangle over the image
			overlay = frame.copy()
			alpha = 0.5
			cv2.rectangle(overlay, (x1, y1), (x2, y2), scolor, thickness=-1)
			cv2.addWeighted(overlay, alpha, frame, 1-alpha, 0, frame)
		
	# Clear previous image and update with new frame
	ax.clear()
	ax.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
	plt.draw()  # Force Matplotlib to update
	plt.pause(0.01)  # Pause for a short moment to allow updates

def move_until_cliff(seconds=None):
	# Set Ultrasonic sensor to face down
	pan_servo.set_angle(80)
	time.sleep(0.6)
	tilt_servo.set_angle(150)
	time.sleep(0.6)
	
	# Move forward until you see cliff (or time elapses)
	start_time = time.time()
	saw_cliff = False
	while True:
		drivetrain.set_motion(speed=SPEED)
		dist = read_sonar()
		# print(dist)
		
		# Check for cliffs
		if dist>MAX_FLOOR_DIST:
			print("CLIFFFFF!!!!!")
			saw_cliff = True
			break
		
		# Check for time
		curr_time = time.time()
		if (curr_time-start_time) > seconds:
			break
		
		time.sleep(0.3)
	
	# Stop
	print('stopped moving')
	drivetrain.set_motion(speed=0)
	time.sleep(0.6)
	
	# Move back a bit
	if saw_cliff:
		print('saw cliff')
		drivetrain.set_motion(speed=-SPEED)
		time.sleep(6.0/IN_PER_SEC) # Move back 6 in
		drivetrain.set_motion(speed=0)
		time.sleep(0.6)
		
		# Turn 180
		turn_degrees(180)
		time.sleep(0.6)

def turn_degrees(degree):
	# 1.7 seconds per 90 degrees at speed 50
	speed = SPEED if degree > 0 else -SPEED
	seconds = abs(degree)/90.0 * SEC_PER_90_DEG
	if seconds < 0.1:
		seconds = 0.1
		
	# Turn amount of degrees
	drivetrain.set_motion(angular_speed=speed)
	time.sleep(seconds)
	drivetrain.set_motion(angular_speed=0)
	time.sleep(0.6)

def move_inches(inches):
	# 4.5 inches per second at speed 50
	speed = SPEED if inches > 0 else -SPEED
	seconds = abs(inches)/IN_PER_SEC
	
	if seconds < 0.1:
		seconds = 0.1
	
	# Turn amount of degrees
	move_until_cliff(seconds)
	

def get_optimal_degree_heading(sonar_data):
	
	data_points = len(sonar_data)
	deg_inc = (SCAN_PAN_MAX-SCAN_PAN_MIN)//data_points
	emphasize = 'center' # Add an extra nudge in this direction
	
	# Find candidate directions
	sonar_data = [-1 if i == 5000 else i for i in sonar_data] # Get rid of 5000s
	max_dist = max(sonar_data)
	candidates = [(sonar_data[i], i) for i in range(data_points) 
					if sonar_data[i] >= max_dist-DIST_MARGIN and sonar_data[i]!=5000]
	candidates = sorted(
			[(sonar_data[i], i) for i in range(data_points) if sonar_data[i] != 5000], 
			key=lambda x: x[0], 
			reverse=True)[:min(3, len(sonar_data))]  # Get the top 3 entries
	
					
	print(f"All candidates: {[i[1] for i in candidates]}")
	# Choose next candidate
	# Prefer candidates that are closer to the middle (depth vs breadth)
	# Consider surroundings (i.e dont go in a direction where you dont fit)
	def good_neighbors(index):
		neighbors = [i for i in [index+1, index-1] if i>0 and i<data_points]
		
		good_neighbors = []
		for i in neighbors:
			if sonar_data[i] > TOO_CLOSE_DIST and sonar_data[i]!=5000:
				good_neighbors.append(i)
			
		# Handle edge cases
		if index+1 >= data_points:
			good_neighbors.append(index+1)
		elif index-1 < 0:
			good_neighbors.append(index-1)
			
		print(f'Good neighbors of {index }: {good_neighbors}')
			
		return good_neighbors
		
	good_candidates = [i for i in candidates if len(good_neighbors(i[1]))>0]
	if len(good_candidates) > 0:
		# Choose best candiate
		print(f"There are good candidates: {good_candidates}")
		good_candidates = sorted(good_candidates, key=lambda x: x[0])
		candidate = good_candidates[-1]
	else:
		# Inside doesn't look good, move towards edges
		print("No good candidates")
		candidate = max([(sonar_data[0], 0), (sonar_data[-1], len(sonar_data) - 1)], 
						key=lambda x: x[0])
		
		if candidate[1] == 0:
			emphasize = 'right'
		else:
			emphasize = 'left'
		
		# Check to see if candidate is still too close
		if candidate[0] <= TOO_CLOSE_DIST:
			# Turn 90 degrees
			if emphasize == 'right':
				return 90
			else:
				return -90

		
	
	# Find relative degree heading (+/- from current position)
	i = candidate[1]
	gn = good_neighbors(i)
	
	if len(gn) == 1:
		if gn[0] > i:
			emphasize = 'left'
		else:
			emphasize = 'right'
	
	if data_points%2 == 0:
		deg_heading = (i - data_points//2) * deg_inc - (deg_inc/2)
	else:
		deg_heading = (i - (data_points//2)) * deg_inc
	
	# Give an extra nudge if needed
	if emphasize == 'left':
		deg_heading -= deg_inc/2
	if emphasize == 'right':
		deg_heading += deg_inc/2
		
	print(f'heading to idx emphasizing {emphasize}:', i)
	return deg_heading



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
        
        if w < 20 and h < 20:
            return image, None

        # Compute center of the rectangle
        center_x, center_y = x + w // 2, y + h // 2

        # Draw the rectangle and center point on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

        # Display center coordinates
        cv2.putText(image, f"({center_x}, {center_y})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        return image, (center_x, center_y)
    
    return image, None  # No green ball found

# Example usage with a live camera feed
if __name__ == "__main__":
	
	
	plt.ion()
	fig, ax = plt.subplots()
		
	

	while True:
		camera.capture()
		frame = camera.image_array
		frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)

		# Process frame
		processed_frame, center = detect_green_ball(frame)

		# Show the processed frame
		ax.clear()
		ax.imshow(cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB))
		plt.draw()  # Force Matplotlib to update
		plt.pause(0.01)  # Pause for a short moment to allow updates

		
            
	cv2.destroyAllWindows()
