from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2

class VideoCamera(object):
    def __init__(self, prototxt, model, confidence=0.2):
        self.prototxt = prototxt
        self.model = model
        self.confidence = confidence
        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

        # initialize the video stream, allow the cammera sensor to warmup,
        # and initialize the FPS counter
        print("[INFO] starting video stream...")
        self.vs = VideoStream(src=0).start()
        
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	                "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	                "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	                "sofa", "train", "tvmonitor"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

        self.fps = FPS().start()

    def __del__(self):
        self.vs.stop()
        self.fps.stop()
        print("[INFO] elapsed time: {:.2f}".format(self.fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
    
    def get_frame(self):
        frame = self.vs.read()
        frame = imutils.resize(frame, width=400)

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        
        # pass the blob through the network and obtain the detections and
	    # predictions
        self.net.setInput(blob)
        detections = self.net.forward()

	    # loop over the detections
        for i in np.arange(0, detections.shape[2]):
	    	# extract the confidence (i.e., probability) associated with
	    	# the prediction
            confidence = detections[0, 0, i, 2]

	    	# filter out weak detections by ensuring the `confidence` is
	    	# greater than the minimum confidence
            if confidence > self.confidence:
	    		# extract the index of the class label from the
	    		# `detections`, then compute the (x, y)-coordinates of
	    		# the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

	    		# draw the prediction on the frame
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)

	    # update the FPS counter
        self.fps.update()
        ret, jpeg = cv2.imencode('.jpg',frame)
        return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
