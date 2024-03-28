from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://tabiturient.ru/globalrating/'
browser.get(url)
sleep(1)
soup = BeautifulSoup(browser.page_source, 'lxml')
table = soup.find('div', class_='obramtop100')
rows = table.find_all('table', class_='listtop100')
info = []
for row in rows:
    data = row.find_all('td')[2]
    indicators = row.find_all('td')[4]
    rating = data.find('span', class_='font2 yesmobile1').text.strip()[1:]
    name = data.find('b').text.strip()
    category = indicators.find_all('b')[0].text.strip()
    score = indicators.find_all('b')[1].text.strip()
    info.append([rating, name, score, category])

column_names = ['Rating', 'Name', 'Grade', 'Category']
df = pd.DataFrame(info, columns=column_names)
print(df.info)
# Создаем папку Data, если она не существует
if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Russia"):
    os.makedirs("Data/Russia")
df.to_excel(f'Data/Russia/Tabiturient.xlsx', index=False)

browser.close()
