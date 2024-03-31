import subprocess


def parse_world():
    site = input()

    if site == "1":
        subprocess.run(["python", "World/The_Higher_Education.py"])
    elif site == "2":
        subprocess.run(["python", "World/QS_World_University_Rankings.py"])
    elif site == "3":
        subprocess.run(["python", "World/CWUR.py"])
    elif site == "4":
        subprocess.run(["python", "World/Shanghai_Ranking.py"])
    elif site == "5":
        subprocess.run(["python", "World/Round_University_Ranking.py"])
    else:
        print("Неверный выбор сайта.")


def parse_africa():
    site = input()

    if site == "1":
        subprocess.run(["python", "Africa/The_Higher_Education.py"])
    elif site == "2":
        subprocess.run(["python", "Africa/SCIMAGO_Institutions_Rankings.py"])
    elif site == "3":
        subprocess.run(["python", "Africa/EduRank.py"])
    elif site == "4":
        subprocess.run(["python", "Africa/US_News.py"])
    elif site == "5":
        subprocess.run(["python", "Africa/Shanghai_Ranking.py"])
    else:
        print("Неверный выбор сайта.")


def parse_arabic():
    site = input()

    if site == "1":
        subprocess.run(["python", "Arabic/The_Higher_Education.py"])
    elif site == "2":
        subprocess.run(["python", "Arabic/UniRanks.py"])
    elif site == "3":
        subprocess.run(["python", "Arabic/EduRank.py"])
    elif site == "4":
        subprocess.run(["python", "Arabic/US_News.py"])
    elif site == "5":
        subprocess.run(["python", "Arabic/Research_com.py"])
    elif site == "6":
        subprocess.run(["python", "Arabic/SCIMAGO_Institutions_Rankings.py"])
    elif site == "7":
        subprocess.run(["python", "Arabic/Shanghai_Ranking.py"])
    else:
        print("Неверный выбор сайта.")


def parse_russia():
    site = input()

    if site == "1":
        subprocess.run(["python", "Russia/RAEX.py"])
    elif site == "2":
        subprocess.run(["python", "Russia/Interfax.py"])
    elif site == "3":
        subprocess.run(["python", "Russia/Tabiturient.py"])
    elif site == "4":
        subprocess.run(["python", "Russia/EduRank.py"])
    elif site == "5":
        subprocess.run(["python", "Russia/Forbes.py"])
    elif site == "6":
        subprocess.run(["python", "Russia/Shanghai_Ranking.py"])
    else:
        print("Неверный выбор сайта.")


def parse_site(region):
    world_sites = ["The Higher Education", "QS World University Rankings",
                   "CWUR", "Shanghai Ranking ARWU", "Round University Ranking"]
    africa_sites = ["The Higher Education", "SCIMAGO Institutions Rankings", "EduRank",
                    "U.S.News", "Shanghai Ranking  (Region -South Africa)"]
    arabic_sites = ["The Higher Education", "UniRanks", "EduRank", "U.S.News",
                    "Research.com", "SCIMAGO Institutions Rankings",
                    "Shanghai Ranking  (Region -Egypt, Pakistan, Iran, Qatar, Saudi Arabia, UAE)"]
    russian_sites = ["RAEX", "Interfax", "Tabiturient", "EduRank", "Forbes",
                     "Shanghai Ranking  (Region -Russia)"]

    if region == "world":
        for number, site in enumerate(world_sites):
            print(f'{number+1}. {site}')
        parse_world()
    elif region == "africa":
        for number, site in enumerate(africa_sites):
            print(f'{number+1}. {site}')
        parse_africa()
    elif region == "arabic":
        for number, site in enumerate(arabic_sites):
            print(f'{number+1}. {site}')
        parse_arabic()
    elif region == "russia":
        for number, site in enumerate(russian_sites):
            print(f'{number+1}. {site}')
        parse_russia()
    else:
        print("Такого региона нет!")


def parse_region():
    print("Выберите регион для парсинга:")
    print("1. Мировой")
    print("2. Африка")
    print("3. Арабские страны")
    print("4. Россия")
    region = input()
    correct_region = ""
    if region == "1":
        correct_region = 'world'
    elif region == "2":
        correct_region = 'africa'
    elif region == "3":
        correct_region = 'arabic'
    elif region == "4":
        correct_region = 'russia'
    else:
        print("Неверный выбор сайта!")
    parse_site(correct_region)


def download_pdfs():
    subprocess.run(["python", "pdf_downloader.py"])
    print('PDF отчеты собраны!')


def main():
    while True:
        print("Выберите действие:")
        print("1. Парсинг")
        print("2. Скачивание PDF")
        print("3. Завершить программу")

        action = input("Введите номер действия:\n")

        if action == "1":
            parse_region()
        elif action == "2":
            download_pdfs()
        elif action == "3":
            print("Программа завершена.")
            break
        else:
            print("Неверный выбор действия.")


if __name__ == "__main__":
    main()
