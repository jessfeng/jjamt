#import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
from multiprocessing import Process
from multiprocessing import Queue
from queue import PriorityQueue
from picamera import PiCamera
import threading
import numpy as np
import argparse
import imutils
import time
import cv2


class ImageReceiver():
    def __init__(self):
        super().__init__()
        self.vs = None

    def execute(self, ImageQueue):
        self.vs = VideoStream(usePiCamera=True).start()

        while True:
            frame = self.vs.read()
            # print(frame)
            if frame is None:
                continue
                
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            #ret, frame = cap.read()
            frame = imutils.resize(frame, width=400)
            ImageQueue.put(frame)
    
    def __del__(self):
        self.vs.stop()

