import requests
import cv2
from PIL import Image, ImageDraw, ImageFont
import time
import numpy as np

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

def send_image_to_server(url, frame):
    # Преобразуем кадр в формат JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)

    # Отправляем кадр на сервер
    response = requests.post(url, files={'image': img_encoded.tobytes()})

    if response.status_code != 200:
        print('Error uploading image')
    elif response.status_code == 200:
        print("All is good")


# URL сервера Flask, замените на актуальный адрес сервера
server_url = 'http://192.168.1.130/api/cam/send'

while True:
    frame = get_image()

    # Запускаем отправку кадров с камеры на сервер
    send_image_to_server(f"{server_url}/1", frame)
    send_image_to_server(f"{server_url}/2", add_gui(frame))

camera.release()
cv2.destroyAllWindows()
