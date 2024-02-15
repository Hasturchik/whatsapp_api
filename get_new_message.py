import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from datetime import datetime
import re

def get_new_message(driver, date):
    chats = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.lhggkp7q.ln8gz9je.rx9719la"))
    )
    messages_list = []
    for chat in chats:
        try:
            time.sleep(0.5)
            chat.location_once_scrolled_into_view
            time.sleep(1)
            chat.click()
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # WebDriverWait(driver, 20).until(
            #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.copyable-text")))
            time.sleep(0.2)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            messages = soup.find_all('div', {'class': 'copyable-text'})
            # print(soup)

            for message in messages:
                if 'data-pre-plain-text' in message.attrs:
                    message_date = message['data-pre-plain-text'].split(']')[0][1:]
                    message_date = datetime.strptime(message_date, "%H:%M, %d.%m.%Y")

                    if message_date > date:
                        text = message.find('span', {'class': '_11JPr selectable-text copyable-text'}).get_text()
                        sender = re.split('] (.+): ', message['data-pre-plain-text'])[-2]

                        # print(text, sender)

                        message_json = {"text": text, "sender": sender}
                        messages_list.append(message_json)
                        print(messages_list)
                else:
                    continue
                    print("Attribute 'data-pre-plain-text' not found in message.")

        except NoSuchElementException:
            continue

    response = requests.post('https://yodepro.bpium.ru/api/webrequest/whatsapptest(начать сессию)', json=messages_list)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")

    # print(messages_list)
