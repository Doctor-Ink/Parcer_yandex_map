import random
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}

user_agents_list_desktop = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
]

def get_source_html(url):

    options = webdriver.ChromeOptions()
    ##### user-agent ########
    # options.add_argument(f"user-agent={random.choice(user_agents_list_desktop)}")
    # disable wevdriver mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    # версия драйвера Index of /105.
    service = Service(
        r'C:\Users\Zver\PycharmProjects\parcer_yandex_map_polyclinics_minsk\chromedriver\chromedriver.exe',
    )
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # open url
        driver.get(url)
        driver.maximize_window()
        time.sleep(1)
        driver.implicitly_wait(30)
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
    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()

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


def get_data(file_path):
    with open(file_path) as file:
        url_list = [url.strip() for url in file.readlines()]

    options = webdriver.ChromeOptions()
    # disable wevdriver mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    # запуск в фоновом режиме
    options.add_argument('--headless')
    # версия драйвера Index of /105
    service = Service(
        r'C:\Users\Zver\PycharmProjects\parcer_yandex_map_polyclinics_minsk\chromedriver\chromedriver.exe',
    )
    driver = webdriver.Chrome(service=service, options=options)

    try:
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



    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()

    return "[INFO] Data collected successfully!"


def main():
    # step 1 - открываем весь список яндекс карточек и записываем html в source_page.html
    # get_source_html(url='https://yandex.by/maps/157/minsk/search/%D0%BF%D0%BE%D0%BB%D0%B8%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0%20%D0%BC%D0%B8%D0%BD%D1%81%D0%BA/?ll=27.603947%2C53.900782&sctx=ZAAAAAgCEAAaKAoSCUxTBDi9jztAEapiKv2E80pAEhIJnZ53Y0Fh0z8RH9sy4Cwluz8iBgABAgMEBSgKOABAnQFIAWI0cmVsZXZfcmFua2luZ19oZWF2eV9jbGlja19tYXBzX2Zvcm11bGE9MC4yOmZtbDg2ODQ5MmI1cmVsZXZfcmFua2luZ19oZWF2eV9yZWxldl9tYXBzX2Zvcm11bGE9MC44OmwzX2RjNjY4ODRqAnVhnQHNzEw9oAEAqAEAvQHFYBI9wgGBAYyvx%2BcD8raf7QO%2FicP%2BA5Hd%2BpQEoZXhpATImOKXBPmj8owFgpGHkQSPhveABJmmzPKXA9LxyuMD25fjiQTBrJ3xA%2Bjr7%2FcDuveNsfUEvK%2BvhASdzIvFBNLs4oIEn6%2Fa6wONx%2B%2B%2FBPerqI4Ewf%2B6%2BAPRn72NBObonfjpA8Hj4In0AeoBAPIBAPgBAIICIdC%2F0L7Qu9C40LrQu9C40L3QuNC60LAg0LzQuNC90YHQuooCEzE4NDEwNjAxNCQxODQxMDU5ODaSAgMxNTeaAgxkZXNrdG9wLW1hcHM%3D&sll=27.603947%2C53.900782&sspn=0.347838%2C0.121804&z=11.8')
    # get_source_html(url='https://yandex.by/maps/10713/yelets/search/%D0%95%D0%BB%D0%B5%D1%86%20%D0%B1%D0%B0%D0%BD%D1%8F/?ll=38.547980%2C52.619062&sll=30.202875%2C55.184219&sspn=0.605621%2C0.194483&z=12')

    # step 2 получаем файл ссылок и файл рейтинга
    # get_items_urls_and_rating(file_path='source_page.html')

    # step 3 проходимся по списку ссылок и достём нужную нам информацию (адрес, телефон и т.д.)
    print(get_data(file_path='item_link.txt'))


if __name__ =='__main__':
    main()




