from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_new_message(driver):
    chats = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.lhggkp7q.ln8gz9je.rx9719la"))
    )
    messages_list = []
    for chat in chats:
        try:
            unread = chat.find_element(By.CSS_SELECTOR, "div._2H6nH span")
            if unread:
                chat.click()

                html = driver.page_source

                # Используем BeautifulSoup для парсинга HTML
                soup = BeautifulSoup(html, 'html.parser')

                # Находим элемент, после которого начинаются непрочитанные сообщения
                unread_start = soup.find('div', {'class': '_1Yy5A focusable-list-item'})

                # Находим все сообщения после плашки о непрочитанных сообщениях
                messages = unread_start.find_all_next('div', {'class': 'copyable-text'})

                # Извлекаем текст из каждого сообщения
                for message in messages:
                    text = message.find('span', {'class': '_11JPr selectable-text copyable-text'}).get_text()
                    print(text)

                    # messages_list.append({"name": name, "text": text})

        except NoSuchElementException:
            continue

    print(messages_list)
    return messages_list, driver
