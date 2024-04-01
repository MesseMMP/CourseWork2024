from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from urllib.parse import urlparse
import os


# Функция для поиска и скачивания PDF-отчетов по ключевым словам
def download_pdf_reports(driver, institute_name, report_url, keywords):
    try:
        if report_url:
            driver.get(report_url)
            pdf_links = driver.find_elements(By.TAG_NAME, 'a')
            institute_folder = os.path.join(data_folder, institute_name)

            if len(pdf_links) > 0:
                if not os.path.exists(institute_folder):
                    os.makedirs(institute_folder)

            for pdf_link in pdf_links:
                try:
                    href = pdf_link.get_attribute('href')
                    if href and href.endswith('.pdf'):
                        # Проверяем, содержит ли ссылка ключевые слова
                        if any(keyword.lower() in href.lower() for keyword in keywords):
                            file_name = os.path.join(institute_folder, href.split('/')[-1])
                            response = requests.get(href, stream=True)
                            with open(file_name, 'wb') as pdf_file:
                                pdf_file.write(response.content)
                except Exception as e:
                    continue
    except Exception as e:
        print(f"Ошибка при обработке института {institute_name}")
        print(e)


# Чтение данных из файла links.xlsx
current_script_path = os.path.abspath(__file__)
current_script_directory = os.path.dirname(current_script_path)
df = pd.read_excel(os.path.join(current_script_directory, 'links.xlsx'))
data_folder = os.path.join(os.path.dirname(__file__), '..', 'PDF_reports')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Запрос ключевых слов у пользователя
keywords_str = input("Введите ключевые слова через запятую: ")
keywords = [kw.strip() for kw in keywords_str.split(',')]

# Инициализация драйвера браузера
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Перебор каждой строки в DataFrame
for index, row in df.iterrows():
    institute_name = str(row[1])
    report_url = str(row[3])
    # Вызов функции для поиска и скачивания PDF-отчетов
    download_pdf_reports(browser, institute_name, report_url, keywords)

# Закрытие драйвера браузера
browser.quit()
