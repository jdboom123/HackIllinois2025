import time
from rover import constants
import signal
from rpi_ws281x import PixelStrip
from rpi_ws281x import Color as PixelColor

if __name__ == '__main__':

    pixel_strip = PixelStrip(
        constants.PIXEL_STRIP['COUNT'], constants.PIXEL_STRIP['PIN'], constants.PIXEL_STRIP['FREQ_HZ'],
        constants.PIXEL_STRIP['DMA'], constants.PIXEL_STRIP[
            'INVERT'], constants.PIXEL_STRIP['BRIGHTNESS'], constants.PIXEL_STRIP['CHANNEL']
    )

    pixel_strip.begin()

    def gracefully_exit(sig, frame):
        pixel_strip.setPixelColor(0, PixelColor(0, 0, 0))
        pixel_strip.setPixelColor(1, PixelColor(0, 0, 0))
        pixel_strip.show()
        exit(0)

    signal.signal(signal.SIGINT, gracefully_exit)

    pixel_strip.setPixelColor(0, PixelColor(255, 0, 0))
    pixel_strip.setPixelColor(1, PixelColor(0, 0, 0))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(0, 255, 0))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(0, 0, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(255, 255, 0))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(0, 255, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(255, 0, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(255, 255, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(0, PixelColor(0, 0, 0))
    pixel_strip.setPixelColor(1, PixelColor(255, 0, 0))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(1, PixelColor(0, 255, 0))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(1, PixelColor(0, 0, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(1, PixelColor(255, 255, 0))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(1, PixelColor(0, 255, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(1, PixelColor(255, 0, 255))
    pixel_strip.show()
    time.sleep(1)

    pixel_strip.setPixelColor(1, PixelColor(255, 255, 255))
    pixel_strip.show()
    time.sleep(1)

    gracefully_exit(None, None)
