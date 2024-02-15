import os
import time
from PIL import Image, ImageOps
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import requests


def get_qr(driver):
    # driver.refresh()
    # 2. Найти определенный элемент на странице.
    # Добавляем ожидание появления элемента на странице
    wait = WebDriverWait(driver, 10)  # Ожидание до 10 секунд
    element = wait.until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="_2I5ox"]//canvas')))  # Используйте правильный XPath
    print("find ready")

    # 3. Извлечь QR-код из этого элемента.
    location = element.location
    size = element.size
    element.screenshot('qrcode.png')

    # Добавляем рамку к изображению
    img = Image.open('qrcode.png')
    img_with_border = ImageOps.expand(img, border=20, fill='white')  # добавляем рамку шириной 20 пикселей
    img_with_border.save('qrcode.png')  # перезаписываем файл с QR-кодом

    print("qr ready")

    # 4. Отправить этот QR-код на API.
    # url = 'https://yodepro.bpium.ru/api/webrequest/qr'  # Замените на URL вашего API
    # files = {'file': open('qrcode.png', 'rb')}
    # response = requests.post(url, files=files)
    # сохраняем QR-код в директорию static
    qr_path = os.path.join('static', 'qrcode.png')
    img_with_border.save(qr_path)

    print("qr ready")

    # возвращаем путь к QR-коду вместо отправки его на API
    return qr_path

