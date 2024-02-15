from datetime import datetime

from flask import Flask, request, jsonify
from get_qr_code import get_qr
from get_new_message import get_new_message
from send_message import send_message
from selenium.webdriver.firefox.options import Options
from threading import Thread, Lock
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



app = Flask(__name__, static_folder='static')

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = None
driver_lock = Lock()
polling_thread = None

def poll_new_messages(date):
    global driver
    while True:
        with driver_lock:
            wait = WebDriverWait(driver, 30)  # 10 seconds timeout
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]/p')))
            get_new_message(driver, date)
        time.sleep(30)  # wait for 1 minute

@app.route('/api', methods=['POST'])
def api():
    global driver, polling_thread
    try:
        data = request.get_json()
        authorisation = data.get('authorisation')
        send_message_data = data.get('send_message')
        end = data.get('end')

        if authorisation is False:
            if driver is None:
                driver = webdriver.Firefox(options=options)
                driver.get('https://web.whatsapp.com/')  # Замените на URL вашего сайта
            with driver_lock:
                qr_path = get_qr(driver)
                qr_url = request.url_root + qr_path  # создаем полный URL для QR-кода
                # 5. Ожидание появления элемента "Защищено сквозным шифрованием" на странице.
                print("Ready")
            if polling_thread is None or not polling_thread.is_alive():
                date = datetime.now()
                # wait = WebDriverWait(driver, 30)  # 10 seconds timeout
                # wait.until(EC.presence_of_element_located(
                #     (By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/div/div/div[3]/span')))
                polling_thread = Thread(target=poll_new_messages, args=(date,))
                polling_thread.start()

            return jsonify({'qr_url': qr_url}), 200  # возвращаем URL QR-кода

        if send_message_data is not None:
            contact = send_message_data.get("contact")
            message = send_message_data.get("message")
            with driver_lock:
                send_message(driver, message, contact)

        if end is True:
            if driver is not None:
                with driver_lock:
                    driver.quit()
                driver = None
            if polling_thread is not None and polling_thread.is_alive():
                polling_thread.join()  # wait for the polling thread to finish
            return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'success': True}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
