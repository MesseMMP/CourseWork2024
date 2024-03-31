from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

url = 'https://www.usnews.com/education/best-global-universities/africa'
browser.get(url)

soup = BeautifulSoup(browser.page_source, 'lxml')

# Нажимаем "Load More" до тех пор, пока не загрузим все объекты
max_number = int(soup.find('div', class_='filter-bar__CountContainer-sc-1glfoa-5 kFwGjm').span.text.strip())
soup = BeautifulSoup(browser.page_source, 'lxml')
table = soup.find('ol', class_='item-list__OrderedListStyled-sc-18yjqdy-0 kFQUBh')
rows = table.find_all('section')
while len(rows) < max_number:
    try:
        print(len(rows))
        button = browser.find_element(By.XPATH,
                                      '//button[@class="button__ButtonStyled-sc-1vhaw8r-1 bGXiGV pager__ButtonStyled-sc-1i8e93j-1 dypUdv type-secondary size-large" and @rel="next"]//span[text()="Load More"]')
        browser.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(browser.page_source, 'lxml')
        table = soup.find('ol', class_='item-list__OrderedListStyled-sc-18yjqdy-0 kFQUBh')
        rows = table.find_all('section')
        sleep(0.5)
    except:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = BeautifulSoup(browser.page_source, 'lxml')
        table = soup.find('ol', class_='item-list__OrderedListStyled-sc-18yjqdy-0 kFQUBh')
        rows = table.find_all('section')
        sleep(0.5)
        continue
info = []
for row in rows:
    name = row.find('h2').text.strip()
    country_and_city = row.find('p', class_='Paragraph-sc-1iyax29-0 eqpdjG')
    country = country_and_city.find_all('span')[0].text.strip()
    city = country_and_city.find_all('span')[-1].text.strip()
    rank = 'Unranked'
    if row.find('ul', class_='RankList__List-sc-2xewen-0 ciVlaM DetailCardGlobalUniversities__StyledRankList-sc-1v60hm5-6 hHAMZU'):
        rank = row.find('ul', class_='RankList__List-sc-2xewen-0 ciVlaM DetailCardGlobalUniversities__StyledRankList-sc-1v60hm5-6 hHAMZU').find_all('li')[0].find('strong').text.strip()[1:]
    other = [x.find('dd').text.strip() for x in row.find('div', class_='DetailCardGlobalUniversities__CardStats-sc-1v60hm5-7 hQaWGH').find_all('div', class_='Box-w0dun1-0 QuickStatHug__Container-hb1bl8-0 bcZeaE fkvuin QuickStatHug-hb1bl8-2 fyaies QuickStatHug-hb1bl8-2 fyaies')]
    info.append([name, rank, country, city, *other])
column_names = ['Name', 'Rank', 'Country', 'City', 'Score', 'Enrollment']
df = pd.DataFrame(info, columns=column_names)
print(df.info)

if not os.path.exists("Data"):
    os.makedirs("Data")
if not os.path.exists("Data/Africa"):
    os.makedirs("Data/Africa")
df.to_excel(f'Data/Africa/US_News.xlsx', index=False)

browser.close()
