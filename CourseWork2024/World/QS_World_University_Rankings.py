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
    url = f'https://www.universityrankings.ch/en/results/QS/{year}'
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    nav = soup.find_all('div', class_='navbar container right')[0]
    pages = nav.find_all('a')
    max_pages = int(pages[4].text.strip())

    info = []
    for i in range(max_pages):
        soup = BeautifulSoup(browser.page_source, 'lxml')
        table = soup.find('table', id='RankingResults').find('tbody')
        rows = table.find_all('tr', itemprop='itemListElement')
        for row in rows:
            world_rank = row.find_all('td')[0].text.strip().split()[0]
            institution = row.find_all('td')[1].text.strip()
            country = row.find_all('td')[2].find('a').get('title').split()[2]
            info.append([world_rank, institution, country])
        if i != max_pages - 1:
            sleep(1)
            next_button = browser.find_element(By.XPATH, "//a[contains(., 'Next')]")
            sleep(1)
            next_button.click()

    column_names = ['World Rank', 'Institution', 'Country']
    df = pd.DataFrame(info, columns=column_names)
    print(df.info())

    if not os.path.exists("Data"):
        os.makedirs("Data")
    if not os.path.exists("Data/World"):
        os.makedirs("Data/World")
    df.to_excel(f'Data/World/QS_Rankings_{year}.xlsx', index=False)

browser.close()
