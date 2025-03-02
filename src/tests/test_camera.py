from rover.camera import Camera
from rover import constants
import time
import signal
import cv2
import matplotlib.pyplot as plt

camera = Camera()
if __name__ == '__main__':
        plt.ion()
        fig, ax = plt.subplots()

        while True:
                camera.capture()
                frame = camera.image_array
                frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)
                
                # Get frame dimensions
                h, w, _ = frame_bgr.shape
                grid_h, grid_w = h // 5, w // 5  # Height & width of each grid section

        
        
                ax.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                plt.pause(0.01)
                ax.clear()
