from get_qr_code import get_qr
from get_new_message import get_new_message
from selenium import webdriver
from send_message import send_message
driver = webdriver.Firefox()  # Используйте путь к своему драйверу, если он не в PATH
driver.get('https://web.whatsapp.com/')  # Замените на URL вашего сайта
while True:
    try:
        new_text = input()
        if new_text == "get_new":
            driver = get_new_message(driver)
        elif new_text == "send_message":
            msg = input("введите текст желаемого сообщения : ")
            name = input("введите имя желаемого контакта : ")
            count = int(input("введите количество сообщений : "))
            send_message(driver, msg, name, count)
        elif new_text == "get_qr":
            driver = get_qr(driver)
        elif new_text == "end":
            if driver is not None:
                driver.close()
            break
    except Exception as e:
        print(f"An error occurred: {e}")
