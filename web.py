from flask import Flask, render_template, Response, request
import cv2
import time
import numpy as np
import socket
import struct
from threading import Thread
import pickle

app = Flask(__name__)

images = [cv2.imread("download.jpg"), cv2.imread("download.jpg")]


@app.route("/")
def hello():
    return render_template("watch.html")


@app.route("/api/cam/get/1")
def get_cam1():
    return Response(gen_img1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/api/cam/get/2")
def get_cam2():
    return Response(gen_img2(), mimetype='multipart/x-mixed-replace; boundary=frame')


def server_run(port, host, num):
    global images
    # Создаем серверное соединение
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    while True:
        try:
            # Принимаем изображения от клиента
            client_socket, client_address = server_socket.accept()
            print("Принято подключение")

            # Получаем размер пакета
            size_data = client_socket.recv(4)
            size = struct.unpack('!i', size_data)[0]

            print(f"Принят размер фото: {size}")

            # Принимаем данные изображения от клиента
            received_data = bytearray()
            while len(received_data) < size:
                data = client_socket.recv(size - len(received_data))
                received_data.extend(data)

            # Десериализуем и отображаем изображение
            frame = pickle.loads(received_data)
            print("Принято изображение")
            images[num] = frame

            cv2.imwrite("sdasdrf.jpg", frame)

            # Закрываем соединение
        except Exception as err:
            print(f"OU ШИТ {err}")
        finally:
            print("Соеденение закрыто")
            client_socket.close()

    server_socket.close()
    cv2.destroyAllWindows()


def gen_img1():
    global images
    while True:
        ret, buffer = cv2.imencode('.jpg', images[0])
        frame = buffer.tobytes()
        time.sleep(2.5)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def gen_img2():
    global images
    while True:
        ret, buffer = cv2.imencode('.jpg', images[1])
        frame = buffer.tobytes()
        time.sleep(2.5)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def run_flask(port, host):
    app.run(port=port, host=host)

if __name__ == "__main__":
    flask = Thread(target=run_flask, args=(80, "0.0.0.0"))
    nonhud = Thread(target=server_run, args=(10, "0.0.0.0", 0))
    hud = Thread(target=server_run, args=(25, "0.0.0.0", 1))
    flask.start()
    nonhud.start()
    hud.start()
