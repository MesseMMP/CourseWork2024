from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://cwur.org/2023.php'
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'lxml')

info = []
table = soup.find('table', id='cwurTable')
rows = table.find('tbody').find_all('tr')
column_names = table.find('thead').text.strip().split('\n')
for row in rows:
    info.append([x.text.strip().replace('\xa0', ' ').replace('\n', ';') for x in row.find_all('td')])

df = pd.DataFrame(info, columns=column_names)
print(df.info)

if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/World"):
    os.makedirs("Data/World")
df.to_excel(f'Data/World/CWUR.xlsx', index=False)