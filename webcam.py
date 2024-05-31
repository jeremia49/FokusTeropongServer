import cv2
import time

class CV2VideoCapture():

    def __init__(self):
        self.cameraActive = False
        self.currentimage = None

    def activateCamera(self):
        self.cam = cv2.VideoCapture(0)
        self.cameraActive = True

    def startStream(self):
        while True:
            time.sleep(1)
            ret, frame = self.cam.read()
            self.currentimage = cv2.imencode('.jpg', frame)[1].tobytes()
        return False

    def release(self):
        self.cameraActive = False
        self.cam.release()
        return True

    
        
            
