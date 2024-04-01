from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep


def switch_year(year):
    if year != 2023:
        button = browser.find_element(By.XPATH, f'//*[@id="__rating_years"]/li[{year - 2019 + 5}]')
        button.click()


browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = f'https://academia.interfax.ru/ru/ratings/?ysclid=lrueu2d01j790594245&page=1&rating=1&year=2023'
browser.get(url)
for year in [2023, 2022, 2021, 2020, 2019]:
    switch_year(year)
    sleep(1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    # Ищем максимальное количество страниц
    navigation = soup.find('nav', class_='pagination')
    max_pages = len(navigation.find_all('a')) - 2
    info = []
    for i in range(max_pages):
        sleep(1)
        next_page_button = browser.find_element(By.CLASS_NAME, 'next')
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        table = soup.find('div', class_='list')
        rows = table.find_all('div', class_='card -rating')
        for j in range(len(rows)):
            row = rows[j]
            position = row.find('div', class_='position').text.strip()
            name = row.find('a', class_='name').text.strip()
            score = row.find('div', class_='score').text.strip()
            rank = [position, name, score]
            info.append(rank)
        next_page_button.click()
    column_names = ['Рейтинг', 'Название', 'Баллы']
    df = pd.DataFrame(info, columns=column_names)
    print(df.info)

    data_folder = os.path.join(os.path.dirname(__file__), '..', 'Data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    russia_folder = os.path.join(data_folder, 'Russia')
    if not os.path.exists(russia_folder):
        os.makedirs(russia_folder)
    file_path = os.path.join(russia_folder, f'Interfax_{year}.xlsx')
    df.to_excel(file_path, index=False)

browser.close()
