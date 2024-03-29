from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
from time import sleep

browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def switch_year(year):
    switch_button = browser.find_element(By.XPATH, f'//*[@id="years"]/option[{14-(2023-year)}]')
    switch_button.click()

url = 'https://roundranking.com/ranking/world-university-rankings.html#world-2023'
browser.get(url)
for year in [2023, 2022, 2021, 2020, 2019]:
    switch_year(year)
    sleep(2)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    info = []
    table = soup.find('table', class_='big-table table-sortable tablesorter')
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        rank = row.find_all('td')[0].text.strip()
        university = row.find_all('td')[1].text.strip()
        score = row.find_all('td')[2].text.strip()
        country = row.find_all('td')[3].text.strip()
        league = row.find_all('td')[5].text.strip()
        info.append([rank, university, score, country, league])
    column_names = ['Rank', 'University', 'Score', 'Country', 'League']
    df = pd.DataFrame(info, columns=column_names)
    print(df.info)
    if not os.path.exists("Data"):
        os.makedirs("Data")
    if not os.path.exists("Data/World"):
        os.makedirs("Data/World")
    df.to_excel(f'Data/World/Round_University_Ranking_{year}.xlsx', index=False)

browser.close()
