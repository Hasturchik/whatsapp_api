from selenium.webdriver.common.by import By
import time

def send_message(driver, msg, name):
    user = driver.find_element(By.XPATH, f'//span[@title = "{name}"]')
    count = 1
    user.click()
    msg_box = driver.find_element(By.XPATH, '//*[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"]')
    for i in range(count):
        for char in msg:
            msg_box.send_keys(char)
            time.sleep(0.1)  # добавьте задержку здесь, 0.1 секунды в этом примере
        button = driver.find_element(By.XPATH, '//*[@class="tvf2evcx oq44ahr5 lb5m6g5c svlsagor p2rjqpw5 epia9gcq"]')
        button.click()

    time.sleep(2)  # Дайте некоторое время для отправки сообщения
    # return driver
