from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
for year in [2023, 2022, 2021, 2020, 2019]:
    url = f'https://raex-rr.com/education/russian_universities/top-100_universities/{year}/'
    browser.get(url)
    sleep(1)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    table = soup.find('table', class_='rrp_table').find('tbody')
    rows = table.find_all('tr')
    info = []
    for row in rows:
        rank = row.find_all('th')[0].text.strip()
        name = row.find_all('th')[1].text.strip()
        other_params = [x.text.strip() for x in row.find_all('td')]
        info.append([rank, name, *other_params])

    column_names = ['№', 'Название', 'Место в предыдущий год', 'Рейтинговый функционал',
                    'Условия для получения качественного образования',
                   'Уровень востребованности выпускников работодателями',
                   'Уровень научно-исследовательской деятельности']
    df = pd.DataFrame(info, columns=column_names)
    print(df.info)
    # Создаем папку Data, если она не существует
    if not os.path.exists("Data"):
        os.makedirs("Data")
    if not os.path.exists("Data/Russia"):
        os.makedirs("Data/Russia")
    df.to_excel(f'Data/Russia/Raex_{year}.xlsx', index=False)

browser.close()
