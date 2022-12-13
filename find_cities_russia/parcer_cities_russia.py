import os
import random
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}

driver = uc.Chrome()
wait = WebDriverWait(driver, 5)


##### user-agent ########

# wait.until(
# EC.visibility_of_element_located(
# (By.CSS_SELECTOR,
#  'div.secondary-accordion:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)'))
#  )
# try:
#     element = wait.until(
#         EC.presence_of_element_located((By.ID, "myDynamicElement"))
#     )
# finally:
#     driver.quit()


def get_source_html(url):
    driver.get(url)
    driver.maximize_window()

    while True:
        # в бесконечном цикле проходим до конца страницы
        div_element_ol = driver.find_elements(By.CLASS_NAME, 'seo-pagination-view')
        print(f'количество вложенных списков - {len(div_element_ol)}')
        divs_element_placeholder = driver.find_elements(By.CLASS_NAME, 'search-snippet-view__placeholder')
        print(f'количество неотрытых карточек - {len(divs_element_placeholder)}')
        for index in range(0, len(divs_element_placeholder), 2):
            actions = ActionChains(driver)
            # driver.implicitly_wait(30)
            actions.move_to_element(divs_element_placeholder[index]).perform()
            time.sleep(0.1)
        trigger = driver.find_elements(By.CLASS_NAME, 'add-business-view__link')
        divs_element_placeholder = driver.find_elements(By.CLASS_NAME, 'search-snippet-view__placeholder')
        if trigger and (len(divs_element_placeholder) == 0):
            with open("source_page.html", mode='w', encoding='utf-8') as file:
                file.write(driver.page_source)
            print(f'File source_page is done')
            break
        else:
            actions = ActionChains(driver)
            actions.move_to_element(div_element_ol[0]).perform()
            time.sleep(1)


def get_items_urls_and_rating(file_path):
    with open(file_path, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    table_content = soup.find_all('li', class_='search-snippet-view')
    link_list = []
    rating_list = []
    for item in table_content:
        link = item.find('a', class_='search-snippet-view__link-overlay _focusable').get('href')
        link_list.append(link)
        try:
            rating = item.find('span', class_='business-rating-badge-view__rating-text _size_m').text.strip()
        except Exception:
            print(f"Информации о рейтинге нет  -  {item.find('div', class_='search-business-snippet-view__address').text} - NONE")
            rating = 'None'
        rating_list.append(rating)

    with open('item_link.txt', mode='w') as file:
        for link in link_list:
            file.write(f"https://yandex.by{link}\n")

    with open('rating.txt', mode='w') as file:
        for item in rating_list:
            file.write(f"{item}\n")
    return "[INFO] Urls collected successfully!"


def get_data(file_path, city):
    with open(file_path) as file:
        url_list = [url.strip() for url in file.readlines()]

    result_list = []
    count = 1
    urls_count = len(url_list)
    for url in url_list:
        print(f"[+]  Processed: {count}/{urls_count}")
        count += 1

        name_list = []
        adress_list = []
        site_list = []
        social_media = []
        phones_company_list = []

        # open url
        driver.get(url)
        driver.maximize_window()
        # driver.implicitly_wait(10)

        # забираем название компании
        try:
            name_company = driver.find_element(By.CLASS_NAME, 'orgpage-header-view__header').text.strip()
            name_list.append(name_company)
        except Exception:
            print('Name company is None')
            name_company = None

        # забираем адресс компании
        try:
            adress_company = driver.find_element(By.CLASS_NAME, 'business-contacts-view__address-link').text.strip()
            adress_list.append(adress_company)
        except Exception:
            adress_company = None

        # Забираем координаты
        my_url = driver.current_url
        # https://yandex.by/maps/org/banya_na_kurskoy/232229006327/?ll=35.432039%2C52.331216&z=9
        some_list = my_url.split('/')[-1].split('.')
        coordinates = [some_list[0][-2:] + '.' + some_list[1][:6] + ', ' + some_list[1][-2:] + '.' + some_list[2][:6]]



        # забираем телефонные номера
        try:
            # ожидаем пока не появится "показать телефон"
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'card-phones-view__more'))
             )
            # нажимаем показать телефон
            if driver.find_elements(By.CLASS_NAME, 'card-phones-view__more') != []:
                driver.find_element(By.CLASS_NAME, 'card-phones-view__more').click()
                time.sleep(0.2)
                # ожидаем пока не появится "стрелка показать все контакты"
                try:
                    wait.until(EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, 'card-phones-view__phone-number'))
                     )
                    driver.find_element(By.CLASS_NAME, 'card-phones-view__phone-number').click()
                except Exception as exc:
                    print('Номер телефона один')
        except Exception as exc:
            print('Телефон не указан')

        try:
            phones_company = driver.find_elements(By.CLASS_NAME, 'card-phones-view__phone-number')
            for phone_number in phones_company:
                phone_company = phone_number.text.strip()
                phones_company_list.append(phone_company)
            print('Phone numbers is done!!!')
        except Exception:
            print('Телефон не указан на сайте')
            phones_company_list = None



        # забираем сайт компании
        try:
            site_company = driver.find_element(By.CLASS_NAME,'business-urls-view__text').text.strip()
            site_list.append(site_company)
        except Exception:
            site_company = None

        # забираем ссылки на соцсети
        try:
            social_medias = driver.find_elements(By.CLASS_NAME, 'business-contacts-view__social-button')
            if social_medias:
                for elem in social_medias:
                    link = elem.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    # print(link)
                    social_media.append(link)
            else:
                social_media = None
        except Exception:
            social_medias = None
        # print(name_company, phones_company_list, adress_company, site_company, social_media)

        result_list.append(
            {
                'name_company': name_company,
                'url_yandex': url,
                'coordinates': coordinates,
                'phone_list': phones_company_list,
                'adress': adress_list,
                'site_company': site_list,
                'social_networks_list': social_media
            }
        )
        # time.sleep(random.randrange(1, 2))
        if count % 10 == 0:
            time.sleep(random.randrange(3, 5))



        with open(f'data\\{city}\\result.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)
    return "[INFO] Data collected successfully!"


def main():
    list_cities = []
    with open('cities.txt', encoding='utf-8') as file:
        reader = file.read()
        for line in reader.split('\n'):
            list_cities.append(line)
        list_cities = list_cities[:-1]
    print(list_cities)

    try:
        for city in list_cities[:3]:
            try:
                os.mkdir(f'data\\{city}')
            except Exception as exc:
                print('Direction is exists')
            print(f'City - {city}')
            # step 1 - открываем весь список яндекс карточек и записываем html в source_page.html
            get_source_html(url=f'https://yandex.by/maps/?text={city}+баня',)
            # step 2 получаем файл ссылок и файл рейтинга
            print(get_items_urls_and_rating(file_path='source_page.html'))
            # step 3 проходимся по списку ссылок и достём нужную нам информацию (адрес, телефон и т.д.)
            print(get_data(file_path='item_link.txt', city=city))
    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()


if __name__ =='__main__':
    main()




