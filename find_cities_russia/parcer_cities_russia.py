import os
import random
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


driver = uc.Chrome()
wait = WebDriverWait(driver, 5)


def time_track(func):
    # функция-декаратор, которая считает время работы
    def surogate(*args, **kwargs):
        start_time = time.time()

        result = func(*args, **kwargs)

        end_time= time.time()
        result_time = end_time - start_time
        print(f'Скрипт отработал - {round(result_time, 2)} секунды')
        return result
    return surogate

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


def get_all_card(file_path):
    with open(file_path, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    table_content = soup.find_all('li', class_='search-snippet-view')
    link_list = []
    for item in table_content:
        link = item.find('a', class_='search-snippet-view__link-overlay _focusable').get('href')
        link_list.append(link)

    with open('item_link.txt', mode='w') as file:
        for link in link_list:
            file.write(f"https://yandex.by{link}\n")
    print("[INFO] Urls collected successfully!")
    return len(link_list)


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
            # print('Name company is None')
            name_company = ''

        # забираем адресс компании
        try:
            adress_company = driver.find_element(By.CLASS_NAME, 'business-contacts-view__address-link').text.strip()
            adress_list.append(adress_company)
        except Exception:
            adress_company = ''

        # Забираем координаты
        my_url = driver.current_url
        # https://yandex.by/maps/org/banya_na_kurskoy/232229006327/?ll=35.432039%2C52.331216&z=9
        some_list = my_url.split('/')[-1].split('.')
        coordinates = [some_list[0][-2:] + '.' + some_list[1][:6] + ', ' + some_list[1][-2:] + '.' + some_list[2][:6]]

        # Забираем рэйтинг компании
        if driver.find_elements(By.XPATH, "//div[@class='orgpage-header-view__wrapper-rating']/div/div/div/div/span[@class='business-rating-badge-view__rating-text _size_m']") != []:
            rating = driver.find_element(By.XPATH,
                                         "//div[@class='orgpage-header-view__wrapper-rating']/div/div/div/div/span[@class='business-rating-badge-view__rating-text _size_m']").text.strip()
        else:
            rating = None

        # забираем телефонные номера
        try:
            # ожидаем пока не появится "показать телефон"
            show_phone = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'card-phones-view__phone'))
            )
            # print(show_phone)
            # нажимаем показать телефон
            if show_phone:
                # print('Нажимаем показать телефон')
                show_phone.click()
                # print('Нажали показать телефон')
                arrow_down = wait.until(EC.presence_of_element_located(
                    (By.XPATH,
                     "//div[@class='card-phones-view _wide']/div/div/div/div/div[@class='card-feature-view__additional']"))
                )
                if arrow_down:
                    # print('Нажимаем показать все телефоны')
                    # arrow_down.click()
                    driver.find_element(By.CLASS_NAME, 'card-phones-view__phone').click()
                    # print('Нажали показать все телефоны!')
                    wait.until(EC.presence_of_element_located(
                        (By.CLASS_NAME, "card-dropdown-view__content"))
                    )
                    time.sleep(0.5)
                    # print('Дождались появления стрелки вверх')
        except Exception as exc:
            pass
            # print('Телефон не указан')
            # print(exc)

        try:
            company_phones = driver.find_elements(By.CLASS_NAME, 'card-phones-view__phone-number')
            for phone_number in company_phones:
                phone_company = phone_number.text.strip()
                phones_company_list.append(phone_company)
            # print('Phone numbers is done!!!')
        except Exception:
            # print('Телефон не указан на сайте')
            phones_company_list = ''

        # забираем сайт компании
        try:
            site_company = driver.find_element(By.CLASS_NAME, 'business-urls-view__text').text.strip()
            site_list.append(site_company)
        except Exception:
            site_company = ''

        # забираем ссылки на соцсети
        try:
            social_medias = driver.find_elements(By.CLASS_NAME, 'business-contacts-view__social-button')
            if social_medias:
                for elem in social_medias:
                    link = elem.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    # print(link)
                    social_media.append(link)
            else:
                social_media = ''
        except Exception:
            social_medias = ''
        # print(name_company, phones_company_list, adress_company, site_company, social_media)

        result_list.append(
            {
                'name_company': name_company,
                'url_yandex': url,
                'coordinates': coordinates,
                'rating': rating,
                'phone_list': phones_company_list,
                'adress': adress_list,
                'site_company': site_list,
                'social_networks_list': social_media
            }
        )
        if count % 10 == 0:
            time.sleep(random.randrange(3, 5))

        with open(f'data\\{city}\\result.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)
    return f"[INFO] {city} - Data collected successfully!"

@time_track
def main():
    list_cities = []
    with open('cities.txt', encoding='utf-8') as file:
        reader = file.read()
        for line in reader.split('\n'):
            list_cities.append(line)
        list_cities = list_cities[:-1]
    print(list_cities)

    count = 0
    try:
        for city in list_cities[51:52]:
            try:
                os.mkdir(f'data\\{city}')
            except Exception as exc:
                print('Direction is exists')
            print(f'City - {city}')
            # step 1 - открываем весь список яндекс карточек и записываем html в source_page.html
            get_source_html(url=f'https://yandex.by/maps/?text={city}+баня',)
            # step 2 получаем файл ссылок и файл рейтинга
            count += get_all_card(file_path='source_page.html')
            # step 3 проходимся по списку ссылок и достём нужную нам информацию (адрес, телефон и т.д.)
            print(get_data(file_path='item_link.txt', city=city))
            print(f'Общее количество карточек ---{count}')

    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()


if __name__ =='__main__':
    main()




