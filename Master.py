import threading
import numpy
from queue import Queue

from ImageReceiver import ImageReceiver
from ObjectDetector import ObjectDetector
# from AlertProcessor import AlertProcessor

class Master():
    def __init__(self):
        super().__init__()

        self.ImageReceiver = ImageReceiver()
        self.ObjectDetector = ObjectDetector()
        # self.AlertProcessor = AlertProcessor()

        self.ImageQueue = Queue()
        # self.ObjectQueue = Queue()

        self.objects = []

    def createObjects(self):
        self.objects.append(threading.Thread(target=self.ImageReceiver.execute, args=(self.ImageQueue, )))
        self.objects.append(threading.Thread(target=self.ObjectDetector.execute, args=(self.ImageQueue, )))
        # self.objects.append(threading.Thread(target=self.AlertProcessor.execute, args=(self.ObjectQueue, )))

    def start(self):
        for any_objects in self.objects:
            any_objects.start()

    # def __del__(self):
    #     for any_objects in self.objects:
    #         any_objects.join()


if __name__ == "__main__":
    master = Master()
    master.createObjects()
    master.start()
