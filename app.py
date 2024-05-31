from io import BytesIO
from flask import Flask, send_file, abort
from webcam import CV2VideoCapture
import threading

app = Flask(__name__)

cv2capture = CV2VideoCapture()
cv2capture.activateCamera()
threading.Thread(target = cv2capture.startStream, daemon=True,).start()

@app.route("/status")
def status():
    return "ready"

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

