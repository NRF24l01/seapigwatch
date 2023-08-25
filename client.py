import requests
import cv2
from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np
import socket
import pickle
import struct

# Открываем камеру
camera = cv2.VideoCapture(0)

def get_image():
    global camera
    # Читаем кадр с камеры
    ret, frame = camera.read()
    cv2.imwrite("nasme.jpg", frame)
    return frame

def add_gui(im):
    img = Image.fromarray(im)

    watermark = Image.open('overlay.png')

    img.paste(watermark, (0, 0), watermark)

    font = ImageFont.truetype('OpenSans-Medium.ttf', size=18)
    draw_text = ImageDraw.Draw(img)
    draw_text.text(
        (28, 95),
        f'{time.ctime(int(time.time()))}',
        font=font,
        fill=('#FFFFFF')
    )
    return np.asarray(img)

def send_image_to_server(port, host, frame):
    # Подключаемся к серверу
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Преобразуем изображение в сериализуемый формат
    serialized_frame = pickle.dumps(frame)

    # Отправляем размер пакета на сервер
    print(len(serialized_frame), struct.pack('!i', len(serialized_frame)))
    client_socket.sendall(struct.pack('!i', len(serialized_frame)))

    # Отправляем изображение на сервер
    client_socket.sendall(serialized_frame)

    # Закрываем соединение
    client_socket.close()


# URL сервера Flask, замените на актуальный адрес сервера
server_url = 'http://192.168.1.130/api/cam/send'

while True:
    frame = get_image()

    # Запускаем отправку кадров с камеры на сервер
    send_image_to_server(10, "127.0.0.1", frame)
    send_image_to_server(25, "127.0.0.1", add_gui(frame))
    time.sleep(1)

camera.release()
cv2.destroyAllWindows()
