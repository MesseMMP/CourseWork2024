from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

for year in [2023, 2022, 2021, 2020, 2019]:
    url = f'https://www.scimagoir.com/rankings.php?sector=Higher+educ.&country=Africa&year={year - 6}'
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    info = []
    table = soup.find('table', id='tbldata')
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        if len(row.find_all('td')) == 0:
            continue
        rank = row.find_all('td')[1].text.strip().split()[0]
        global_rank = row.find_all('td')[1].text.strip().split()[1].replace('(', '').replace(')', '')
        institution = row.find_all('td')[2].text.strip()
        country = row.find_all('td')[3].text.strip()
        info.append([rank, global_rank, institution, country])
    column_names = ['Rank', 'Global Rank', 'Institution', 'Country']
    df = pd.DataFrame(info, columns=column_names)
    print(df.info)
    if not os.path.exists("Data"):
        os.makedirs("Data")
    if not os.path.exists("Data/Africa"):
        os.makedirs("Data/Africa")
    df.to_excel(f'Data/Africa/SCIMAGO_Institutions_Rankings_{year}.xlsx', index=False)

browser.close()