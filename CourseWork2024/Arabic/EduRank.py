from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
url = 'https://edurank.org/geo/ae/'
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

column_names = ['Name', 'City', 'Asia Rank', 'World Rank']
df = pd.DataFrame(info, columns=column_names)
print(df.info)

# Путь к папке Data
data_folder = os.path.join(os.path.dirname(__file__), '..', 'Data')

# Проверка существования папки Data и ее создание, если она не существует
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Путь к папке Russia внутри папки Data
arabic_folder = os.path.join(data_folder, 'Arabic')

# Проверка существования папки Arabic внутри папки Data и ее создание, если она не существует
if not os.path.exists(arabic_folder):
    os.makedirs(arabic_folder)

# Путь к файлу EduRank.xlsx в папке Arabic
file_path = os.path.join(arabic_folder, 'EduRank.xlsx')

# Сохранение DataFrame в файл
df.to_excel(file_path, index=False)

browser.close()
