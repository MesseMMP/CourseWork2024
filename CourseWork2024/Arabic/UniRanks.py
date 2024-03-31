from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.uniranks.com/ranking?region=Arab+World'
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'lxml')
rows = soup.find_all('div', 'row mb-2 uni-listing-wrapper md-hidden')
navigation = soup.find('ul', class_='pagination')
max_pages = int(navigation.find_all('li')[-2].text.strip())
info = []
for page in range(1, max_pages + 1):
    url = f'https://www.uniranks.com/ranking?region=Arab+World&page={page}'
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    rows = soup.find_all('div', 'row mb-2 uni-listing-wrapper md-hidden')
    for row in rows:
        name = row.find('a').text.strip()
        other_info = row.find('div', class_='mb-6 px-2')
        current_info = [x.text.strip() if x else '' for x in other_info.find_all('span', class_='text-muted')]
        info.append([name, *current_info])
column_names = ['Name', 'Rank', 'Score', 'Location']
df = pd.DataFrame(info, columns=column_names)
print(df.info)

if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Arabic"):
    os.makedirs("Data/Arabic")
df.to_excel(f'Data/Arabic/UniRanks.xlsx', index=False)

browser.close()
