from io import BytesIO
from flask import Flask, send_file, abort, jsonify
from webcam import CV2VideoCapture
import threading
from sensor import Sensor 

app = Flask(__name__)

cv2capture = CV2VideoCapture()
cv2capture.activateCamera()

sensor = Sensor()

threading.Thread(target = cv2capture.startStream, daemon=True,).start()
threading.Thread(target = sensor.start_sensor, daemon=True,).start()

@app.route("/")
def home():
    return "Server is ready and up"

@app.route("/status")
def status():
    return sensor.status

@app.route('/image')
def image():
    img = cv2capture.currentimage
    if(img == None):
        return abort(404)
    else:
        buffer = BytesIO()
        buffer.write(img)
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype='image/jpeg'
        )

