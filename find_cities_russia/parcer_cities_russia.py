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

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
useragent = UserAgent()
options = webdriver.FirefoxOptions()
# disable wevdriver mode
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f"user-agent={useragent.random}")
service = Service(
    r'C:\Users\Zver\PycharmProjects\parcer_yandex_map_polyclinics_minsk\Firefoxdriver\geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 2)


def object_webdriver(url, func):
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

    # open url
    driver.get(url)
    driver.maximize_window()
    func()




def get_source_html(driver, url):
        while True:
            # в бесконечном цикле проходим до конца страницы
            div_element_ol = driver.find_elements(By.CLASS_NAME, 'seo-pagination-view')
            print(f'количество вложенных списков - {len(div_element_ol)}')
            divs_element_placeholder = driver.find_elements(By.CLASS_NAME, 'search-snippet-view__placeholder')
            print(f'количество неотрытых карточек - {len(divs_element_placeholder)}')
            for index in range(0, len(divs_element_placeholder), 2):
                actions = ActionChains(driver)
                driver.implicitly_wait(30)
                actions.move_to_element(divs_element_placeholder[index]).perform()
                time.sleep(1)
            print(len(divs_element_placeholder))
            trigger = driver.find_elements(By.CLASS_NAME, 'add-business-view__link')
            if trigger and (len(divs_element_placeholder) == 0):
                with open("source_page.html", mode='w', encoding='utf-8') as file:
                    file.write(driver.page_source)
                break
            else:
                actions = ActionChains(driver)
                actions.move_to_element(div_element_ol[0]).perform()
                time.sleep(3)


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
            print(f'Информации о рейтинге нет  -  {item}')
            rating = 'None'
        rating_list.append(rating)

    with open('item_link.txt', mode='w') as file:
        for link in link_list:
            file.write(f"https://yandex.by{link}\n")

    with open('rating.txt', mode='w') as file:
        for item in rating_list:
            file.write(f"{item}\n")
    return "[INFO] Urls collected successfully!"


def get_data(driver, file_path):
    with open(file_path) as file:
        url_list = [url.strip() for url in file.readlines()]



    result_list = []
    count = 1
    urls_count = len(url_list)
    for url in url_list:
        name_list = []
        adress_list = []
        site_list = []
        social_media = []

        # open url
        # print(url)
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)
        driver.implicitly_wait(30)

        # забираем название компании
        try:
            name_company = driver.find_element(By.CLASS_NAME, 'orgpage-header-view__header').text.strip()
            name_list.append(name_company)
        except Exception:
            name_company = None

        # забираем телефонные номера
        phones_company_list = []
        try:
            driver.find_element(By.CLASS_NAME, 'card-phones-view__more').click()
            time.sleep(1)
            driver.find_element(By.CLASS_NAME, 'card-feature-view__additional').click()
            time.sleep(1)
        except Exception as exc:
            print('Не найден селектор')
        try:
            phones_company = driver.find_elements(By.CLASS_NAME, 'card-phones-view__phone-number')
            for phone_number in phones_company:
                phone_company = phone_number.text.strip()
                phones_company_list.append(phone_company)
        except Exception:
            phone_company = None

        # забираем адресс компании
        try:
            adress_company = driver.find_element(By.CLASS_NAME, 'business-contacts-view__address-link').text.strip()
            adress_list.append(adress_company)
        except Exception:
            adress_company = None

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
                'url_company': url,
                'phone_list': phones_company_list,
                'adress': adress_list,
                'site_company': site_list,
                'social_networks_list': social_media
            }
        )
        time.sleep(random.randrange(1, 2))
        if count % 10 == 0:
            time.sleep(random.randrange(3, 5))

        print(f"[+]  Processed: {count}/{urls_count}")

        count += 1

        with open('result1.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file, indent=4, ensure_ascii=False)
    return "[INFO] Data collected successfully!"

def func1():
    print(f'function ONE is done!')

def main():
    list_cities = []
    with open('cities.txt', encoding='utf-8') as file:
        reader = file.read()
        for line in reader.split('\n'):
            list_cities.append(line)
        list_cities = list_cities[:-1]
    print(list_cities)

    try:
        for city in list_cities[:10]:
            print(f'City - {city}')
            # step 1 - открываем весь список яндекс карточек и записываем html в source_page.html
            object_webdriver(url=f'https://yandex.by/maps/?text={city}+баня', func=func1)
    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()

    # step 2 получаем файл ссылок и файл рейтинга
    # get_items_urls_and_rating(file_path='source_page.html')

    # step 3 проходимся по списку ссылок и достём нужную нам информацию (адрес, телефон и т.д.)
    # print(get_data(file_path='item_link.txt'))


if __name__ =='__main__':
    main()




