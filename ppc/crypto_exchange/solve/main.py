import time

from requests import get
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from config_parser import headers

# Качаем драйвер и помещаем его в корневую папку проекта
options = Options()
options.add_argument(headers)
driver = webdriver.Chrome()

base_url = "YOU_URL" # "http://host:port"
""" Продумываем стратегию для минимизации количества итераций, засовываем в цикл.
 Флаг доступен, когда накопим 10000$ """

response = get(base_url)
driver.set_window_size(2560, 1440)


def registration():
    driver.get(base_url)
    actions = ActionChains(driver)
    nickname = driver.find_element(By.CSS_SELECTOR,
                                   "#root > div > div > form > div:nth-child(2) > label > input[type=text]")
    email = driver.find_element(By.CSS_SELECTOR,
                                '#root > div > div > form > div:nth-child(1) > label > input[type=text]')
    password = driver.find_element(By.CSS_SELECTOR,
                                   '#root > div > div > form > div:nth-child(3) > label > input[type=password]')
    nickname_val = nickname.send_keys("you_nick")
    time.sleep(2)

    email_val = email.send_keys("your_email")
    time.sleep(2)

    password_val = password.send_keys("your_pwd")
    time.sleep(2)

    key_register = driver.find_element(By.CSS_SELECTOR, "#root > div > div > form > button")
    key_register.click()
    time.sleep(2)

    driver.refresh()
    time.sleep(5)


def iterations():
    def get_balance():
        balance_text = driver.find_element(By.XPATH, '//*[@id="root"]/h1[1]/strong').text
        return float(balance_text)

    balance = get_balance()
    while balance < 13:
        buy_tron = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/button[1]').click()
        time.sleep(0.5)  # увеличиваем задержку
        sell_tron = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/button[2]').click()
        time.sleep(0.5)
        balance = get_balance()

    while balance < 10000:
        buy_bitcoin = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/button[1]').click()
        time.sleep(0.5)
        sell_bitcoin = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/button[2]').click()
        time.sleep(0.5)
        balance = get_balance()

    flag = driver.find_element(By.XPATH, '//*[@id="root"]/button').click()
    time.sleep(25)


registration()
iterations()
