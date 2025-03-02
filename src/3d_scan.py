from rover.servo import Servo
from rover import constants
from rover.sonar import Sonar
from rover.sonar_led import SonarLEDS
from rover.camera import Camera

import time
import signal
import cv2
import matplotlib.pyplot as plt

pan_servo = Servo(constants.CAMERA_SERVOS['pan'])
tilt_servo = Servo(constants.CAMERA_SERVOS['tilt'])
sonar = Sonar()
sonar_leds = SonarLEDS()
camera = Camera()

SCAN_PAN_MIN, SCAN_PAN_MAX, SCAN_PAN_DELTA = 35, 130, 10
SCAN_TILT_MIN, SCAN_TILT_MAX, SCAN_TILT_DELTA = 80, 135, 10

# Color Gradient from Red to Green + White
COLORS = [0xd91a1a, 0xd46a19, 0xd49c19, 0xd4b519, 0x42d419, 0x19d4c7, 0xFFFFFF]	
DIST_PER_COLOR = 160	


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

if __name__ == '__main__':

	def signal_handler(sig, frame):
		set_leds(0x000000)
		#pan_servo.set_angle(90)
		#tilt_servo.set_angle(90)
		exit(0)

	signal.signal(signal.SIGINT, signal_handler)
	
	
	plt.ion()
	fig, ax = plt.subplots()
	
	data = full_scan()
	
	print("Ultrasonic data:")
	for line in data:
		print(line)
		
	show_camera_frame(data, fig, ax)
	input()
		
	'''
	num = 90
	while num>=0:
		num = int(input())
		tilt_servo.set_angle(num)
	'''
