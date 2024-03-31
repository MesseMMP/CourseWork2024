from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://datawrapper.dwcdn.net/en9ux/1/'
browser.get(url)

soup = BeautifulSoup(browser.page_source, 'lxml')

info = []
for i in range(10):
    soup = BeautifulSoup(browser.page_source, 'lxml')
    table = soup.find('table').find('tbody')
    rows = table.find_all('tr')
    for j in range(len(rows)):
        row = rows[j]
        name = row.find('th').text.strip()
        other_params = [x.text.strip() for x in row.find_all('td')]
        info.append([name, *other_params])
    if i != 9:
        sleep(1)
        next_page_button = browser.find_element(By.CLASS_NAME, 'next.svelte-1ya2siw')
        sleep(1)
        next_page_button.click()
        sleep(1)

column_names = ['Название', 'Востребованность выпускников', 'Качество нетворкинга',
                'Международная репутация', 'Качество преподавания', 'Фактор Forbes', 'Итог']
df = pd.DataFrame(info, columns=column_names)
print(df.info)
if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Russia"):
    os.makedirs("Data/Russia")
df.to_excel(f'Data/Russia/Forbes.xlsx', index=False)

browser.close()
