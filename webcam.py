import cv2
import time
import numpy as np
from detection import Detection
from io import BytesIO

class CV2VideoCapture():

    def __init__(self):
        self.cameraActive = False
        self.currentimage = None
        self.currentDetectionStatus = True
        self.detection = Detection()
        self.density = 0
        self.reconsturctionerr = 0
        self.shouldrunInference = False

    def activateCamera(self):
        self.cam = cv2.VideoCapture(0)
        self.cameraActive = True
    
    def refreshCamera(self):
        self.cam = cv2.VideoCapture(0)

    def startStream(self, alert):
        while True:
            time.sleep(1)
            ret, frame = self.cam.read()
            if(ret == False):
                self.refreshCamera()
                continue
            self.currentimage = cv2.imencode('.jpg', frame)[1].tobytes()
            
            if(self.shouldrunInference):
                density,reconstruct_err = self.detection.checkAnomaly(BytesIO(self.currentimage))
                self.density = density
                self.reconsturctionerr = reconstruct_err
                if density < 7000 or reconstruct_err > 0.02:
                    self.currentDetectionStatus = False
                    print("Deteksi Salah")
                else:
                    self.currentDetectionStatus = True
                    print("Deteksi Benar")


            # Lakukan Inference
            
            if(not self.currentDetectionStatus):
               alert()
            
            


    def release(self):
        self.cameraActive = False
        self.cam.release()
        return True

            
