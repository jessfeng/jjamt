# net.forward() - blocking operation
#real-time object detection + OpenCV

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

from Buzzer import Buzzer

#if frame has what we're looking for or not
#net = the neural network obj
#inputQueue = FIFO queue of frames
#outputQueue = FIFO queue of detections that will move onto main thread

def classify_frame(net, inputQueue, outputQueue):
    while True:
        #check if frame present in input queue
        if not inputQueue.empty():
            #grab frame from input queue, resize, + construct blob from it
            frame = inputQueue.get()
            frame = cv2.resize(frame, (300,300))
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (300,300), 127.5) #image, scalefactor, size, mean)

            #set blob as input to deep learning obj (net) + obtain detections
            net.setInput(blob)
            detections = net.forward()

            #write detections to output queue
            outputQueue.put(detections)


#argument parse and parse arguments command line
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required = True,
    help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required = True,
    help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


#initialization
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3));

#load serialized model from disk (neural network model)
print("[INFO] loading model...")
#IDK
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])


#init input queue (frames), output queues (detections) + list of actual
#detections returned by child process
inputQueue = Queue(maxsize=1) #populated by parent, processed by child
outputQueue = Queue(maxsize=1) #populated by child, processed by parent (output from processing input)
detections=None

#construct child process *independent* from main process of execution
print("[INFO] starting process...")
p = Process(target=classify_frame, args=(net, inputQueue, outputQueue,))
p.daemon = True
p.start()

#init video stream, allow camera warmup + init FPS counter
print("[INFO] starting stream...")
#cap=cv2.VideoCapture(0)
vs = VideoStream(usePiCamera=True).start()
time.sleep(1.0)
fps=FPS().start()
area = 0
my_priority_queue = PriorityQueue(maxsize=0)

buzzer = Buzzer()
# playRightBuzzer = threading.Thread(target=buzzer.playRightBuzzer, args=())
# lightLeftLED = threading.Thread(target=buzzer.lightLeftLED, args=())
# closeBuzzer = threading.Thread(target=buzzer.closeBuzzer, args=())
# closeLED = threading.Thread(target=buzzer.closeLED, args=())

# def danger(isTrue):
    # if (isTrue):
        # playRightBuzzer.start()
        # lightLeftLED.start()
    # else:
        # closeBuzzer.start()
        # closeLED.start()

#loop over frames of vid stream
while True:
    #grab frame from threaded vidstream, resize + dimensions!!
    frame = vs.read()
    # frame = cv2.rotate(frame,cv2.ROTATE_180)
    #ret, frame = cap.read()
    frame = imutils.resize(frame, width=400)
    (fH, fW) = frame.shape[:2]

    #if input queue IS empty, give current frame to classify
    if inputQueue.empty():
        inputQueue.put(frame)
    #if output queue IS NOT empty, grab detections
    if not outputQueue.empty():
        detections = outputQueue.get()

    
    #check to see if detections are not None (if None, draw detections on frame)
    if detections is not None:
        #ret, img=cap.read()
        #loop over detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence`
            # is greater than the minimum confidence
            if confidence < args["confidence"]:
                continue

            # otherwise, extract the index of the class label from
            # the `detections`, then compute the (x, y)-coordinates
            # of the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            dims = np.array([fW, fH, fW, fH])
            box = detections[0, 0, i, 3:7] * dims
            # if (idx==15) and confidence * 100 > 90:
                # try:
                    # areaBef = ((endY-startY)*(endX-startX))
                # except:
                    # areaBef = -99;
            (startX, startY, endX, endY) = box.astype("int")
            
            # only run once 
            if area == 0 and idx == 15 and confidence * 100 > 80:
                area = -(endY-startY)*(endX-startX)
                my_priority_queue.put(area)
                continue
                
            if idx==5 or idx==6 or idx==7 or idx==9 or idx==15:
                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                if (idx==15) and confidence * 100 > 80:
                    current_area = -(endY-startY)*(endX-startX)
                    # my_priority_queue.put(current_area)
                    
                    largest_area = my_priority_queue.get()
                    # print("The ratio of largest area is {}". format(largest_area / (300*300)))
                    
                    if (-current_area > -largest_area and -current_area > 300 * 300 / 3):
                        print("Danger!!")
                        buzzer.execute("playRightBuzzer")
                        buzzer.execute("lightLeftLED")
                        #print("last area is {}".format(current_area))
                        area = 0
                        
                    elif (-current_area < -largest_area and -largest_area > 300 * 300 / 3):
                        print("less Danger!!")
                        buzzer.execute("lightLeftLED")
                        #print("last area is {}".format(largest_area))
                        area = 0
                        my_priority_queue.put(current_area)
                        
                    elif (-current_area > -largest_area and -current_area < 300 * 300 / 3):
                        my_priority_queue.put(largest_area)
                        
                    else:
                        #print("last area is {}".format(largest_area))
                        #print("current area is {}".format(current_area))
                        #print("different area is {}".format(largest_area - current_area))
                        my_priority_queue.put(current_area)
                        # my_priority_queue.put(current_area)
                        
                    
                    # if (((endY-startY)*(endX-startX))) > 45000 and (areaBef != -99) and (((endY-startY)*(endX-startX))/(areaBef) > 1.2):
                        # print("RUN!!!")
                        # print(CLASSES[idx])
                        # print ("end: " + str((endY-startY)*(endX-startX)))
                        # print ("beg: " + str(areaBef))
                   
            #cv2.imshow("Frame", frame)
            cv2.waitKey(5)
            key = cv2.waitKey(5)
            
            
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            # update the FPS counter
            fps.update()
    time.sleep(0.3)

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
