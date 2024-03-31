from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

url = 'https://www.timeshighereducation.com/sub-saharan-africa-university-rankings'
browser.get(url)
soup = BeautifulSoup(browser.page_source, 'lxml')
navigation = soup.find('ul', class_='pagination')
max_pages = int(navigation.find_all('li')[-2].text.strip())
table = soup.find('table', id='datatable-1')
head = table.find('thead').find_all('th')
column_names = [x.text.strip() for x in head]
info = []
for page in range(max_pages):
    soup = BeautifulSoup(browser.page_source, 'lxml')
    table = soup.find('table', id='datatable-1')
    rows = table.find('tbody').find_all('tr', role='row')
    for row in rows:
        rank = row.find_all('td')[0].text.strip()
        if rank[0] == '=':
            rank = rank[1:]
        name_and_country = ''
        if row.find_all('td')[1].find('a', class_='ranking-institution-title') and \
                row.find_all('td')[1].find('div', class_='location'):
            name_and_country = row.find_all('td')[1].find('a',
                                                          class_='ranking-institution-title').text.strip() + ' / ' + \
                               row.find_all('td')[1].find('div', class_='location').text.strip()
        other_info = [x.text.strip() if x else '' for x in row.find_all('td')[2:]]
        current_info = [rank, name_and_country] + other_info
        info.append(current_info)
    if page != max_pages - 1:
        while True:
            try:
                next_button = browser.find_element(By.CSS_SELECTOR, 'li.paginate_button.next.mz-page-processed a')
                next_button.click()
                break
            except:
                sleep(0.5)  # Пауза в пол секунды и повторяем нажатие
df = pd.DataFrame(info, columns=column_names)
print(df.info)
if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Africa"):
    os.makedirs("Data/Africa")
df.to_excel(f'Data/Africa/The_Higher_Education.xlsx', index=False)

browser.close()
