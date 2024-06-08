import cv2
import time

class CV2VideoCapture():

    def __init__(self):
        self.cameraActive = False
        self.currentimage = None
        self.currentDetectionStatus = True

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
            
            # Lakukan Inference
            
            if(not self.currentDetectionStatus):
               alert()
            
            


    def release(self):
        self.cameraActive = False
        self.cam.release()
        return True

            
