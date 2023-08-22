from flask import Flask, render_template, Response, request
import cv2
import time
import numpy as np

app = Flask(__name__)

image1 = cv2.imread("download.jpg")
image2 = cv2.imread("download.jpg")

@app.route("/")
def hello():
    return render_template("watch.html")


@app.route("/api/cam/get/1")
def get_cam1():
    return Response(gen_img1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/api/cam/get/2")
def get_cam2():
    return Response(gen_img2(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/cam/send/1', methods=['POST'])
def upload_video1():
    global image1
    files = request.files
    if 'image' not in files:
        return 'No image found', 400

    image = files['image']
    image_np = np.frombuffer(image.read(), np.uint8)
    image1 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    return 'Image uploaded successfully'

@app.route('/api/cam/send/2', methods=['POST'])
def upload_video2():
    global image2
    files = request.files
    if 'image' not in files:
        return 'No image found', 400

    image = files['image']
    image_np = np.frombuffer(image.read(), np.uint8)
    image2 = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    return 'Image uploaded successfully'

def gen_img1():
    global image1
    while True:
        ret, buffer = cv2.imencode('.jpg', image1)
        frame = buffer.tobytes()
        time.sleep(2.5)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_img2():
    global image2
    while True:
        ret, buffer = cv2.imencode('.jpg', image2)
        frame = buffer.tobytes()
        time.sleep(2.5)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0", debug=True)
