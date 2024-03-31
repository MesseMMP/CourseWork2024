from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://research.com/university-rankings/best-global-universities/sa'
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'lxml')
table = soup.find('div', id='rankingItems')
rows = table.find_all('div', class_='cols university-item rankings-content__item show')
info = []
for row in rows:
    global_rank = row.find('span', class_='col col--3 py-0 px-0 position border').text.strip().split('\n')[0]
    national_rank = row.find('span', class_='col col--3 py-0 px-0 position').text.strip().split('\n')[0]
    name = row.find('h4').text.strip()
    country = row.find('span', class_='sh').text.strip()
    scholars = row.find('span', class_='ranking no-wrap').text.strip()
    H_index = row.find_all('span', class_='ranking no-wrap')[1].text.strip()
    publications = row.find('span', class_='col col--3 py-0 ranking no-wrap').text.strip()
    info.append([name, country, global_rank, national_rank, scholars, publications, H_index])
column_names = ['Name', 'Country', 'World Rank', 'National Rank', 'Scholars', 'Publications', 'H-Index']

df = pd.DataFrame(info, columns=column_names)
print(df.info)
if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Arabic"):
    os.makedirs("Data/Arabic")
df.to_excel(f'Data/Arabic/Research_com.xlsx', index=False)

browser.close()
