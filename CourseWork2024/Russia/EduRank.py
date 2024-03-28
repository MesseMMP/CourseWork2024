from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://edurank.org/geo/ru/'
browser.get(url)

soup = BeautifulSoup(browser.page_source, 'lxml')
table = soup.find_all('div', class_='container-pad-mob')[1]
rows = table.find_all('div', class_='block-cont pt-4 mb-4')
info = []
for row in rows:
    name = row.find('h2').text.strip()
    name = re.search(r'\d+\.\s(.+)', name).group(1)
    city = row.find('div', class_='uni-card__geo text-center').text.strip()
    ranks = [x.text.strip().split()[0][1:] for x in row.find_all('div', class_='uni-card__rank')]
    info.append([name, city, *ranks])

column_names = ['Название', 'Город', 'Рейтинг в Европе','Рейтинг в мире']
df = pd.DataFrame(info, columns=column_names)
print(df.info)

if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Russia"):
    os.makedirs("Data/Russia")
df.to_excel(f'Data/Russia/EduRank.xlsx', index=False)
