import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
def get_qr(driver):
    driver.refresh()
    # 2. Найти определенный элемент на странице.
    # Добавляем ожидание появления элемента на странице
    wait = WebDriverWait(driver, 10) # Ожидание до 10 секунд
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_2I5ox"]//canvas'))) # Используйте правильный XPath
    print("find ready")

    # 3. Извлечь QR-код из этого элемента.
    location = element.location
    size = element.size
    element.screenshot('qrcode.png')
    print("qr ready")

    # 4. Отправить этот QR-код на API.
    url = 'https://mosmap.bpium.ru/api/webrequest/test' # Замените на URL вашего API
    files = {'file': open('qrcode.png', 'rb')}
    response = requests.post(url, files=files)
    print("get ready")
    time.sleep(15)

    # 5. Ожидание появления элемента "Защищено сквозным шифрованием" на странице.
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[4]/div/div/div[3]/span')))
    print("Ready")

    return driver
