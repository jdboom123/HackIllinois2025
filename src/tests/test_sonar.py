from rover.sonar import Sonar
from rover.sonar_led import SonarLEDS
import time

sonar = Sonar()
sonar_leds = SonarLEDS()
COLORS = [0xd91a1a, 0xd46a19, 0xd49c19, 0xd4b519, 0x42d419, 0x19d4c7, 0xFFFFFF]	
	
def set_leds(color):
	# Set both LED colors the same
	sonar_leds.left.setPixelColor(color)
	sonar_leds.right.setPixelColor(color)


def read_sonar():
	dist = sonar.get_distance()
	
	if dist < 128:
		set_leds(COLORS[0])
	elif dist < 128*2:
		set_leds(COLORS[1])
	elif dist < 128*3:
		set_leds(COLORS[2])
	elif dist < 128*4:
		set_leds(COLORS[3])
	elif dist < 128*5:
		set_leds(COLORS[4])
	elif dist == 5000:
		set_leds(COLORS[6])
	else:
		set_leds(COLORS[5])
		
	return dist

while True:
    print(read_sonar())
    time.sleep(1)
