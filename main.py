from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import logging
from logging.handlers import RotatingFileHandler
from engine import *
from driver import create_driver


CITIES = ['воскресенск', ]
RESULT_FILE = 'data/result.xlsx'
FILE_REQUESTS = 'requests.txt'
COUNT = 0
MAX_COUNT = 40

# Initialize logging
logger = logging.getLogger(__name__)
file_handler = RotatingFileHandler(filename='bot.log', encoding='utf-8', maxBytes=1048576, backupCount=3)
file_handler.setLevel(logging.WARNING)
console = logging.StreamHandler()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(handlers=[file_handler, console], format=FORMAT, level=logging.INFO)


def page_crawl(url):
    global COUNT
    global MAX_COUNT
    driver = create_driver(user_id=3)
    try:
        # open url
        driver.get(url)
        action = ActionChains(driver)
        wait = WebDriverWait(driver, 1)
        crawler = driver.find_element(By.CLASS_NAME, 'scroll__scrollbar-thumb')

        df = pd.DataFrame(columns=['Название', 'Адрес', 'Контакты', 'Сайт', 'Соц сети', 'Ссылка', 'Координаты',])
        cur_card = 0

        while COUNT <= MAX_COUNT:
            #  получаем кол-во доступных карточек
            count_cards = driver.find_elements(By.XPATH, "//div[contains(@class,'search-business-snippet-view__title')]")
            logger.info("number of available cards - %s ", len(count_cards))
            for card in range(cur_card, len(count_cards)):
                try:
                    count_cards[cur_card].click()
                    # time.sleep(1)
                    data = get_data(driver=driver, card=count_cards[cur_card])

                    # Adding data to the DataFrame
                    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                    cur_card += 1
                    COUNT += 1

                except Exception as exc:
                    logger.exception("I don't push cards - %s %s", count_cards[cur_card], exc.args)

                if COUNT >= MAX_COUNT:
                    break

            if COUNT >= MAX_COUNT:
                break
            try:
                # ждун на неоткрытые карточки
                waiting_man = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-snippet-view__placeholder')))
                action.move_to_element(waiting_man).perform()
                print("Move to a closed cards")
            except TimeoutException as exc:
                print(f"No hidden elements / waiting_man {exc}")
                action.drag_and_drop_by_offset(crawler, 0, 5)
                action.perform()
                print('Scroll down')

                # ждун на ДОБАВИТЬ ОРГАНИЗАЦИЮ после прокрутки всех карточек
                # кнопка добавить организацию которая появляется после прокрутки всего списка
                try:
                    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'add-business-view__link')))
                    divs_placeholder = driver.find_elements(By.CLASS_NAME, 'search-snippet-view__placeholder')
                    if len(divs_placeholder) == 0:
                        print('**********FINISH****************')
                        break
                except Exception as exc:
                    print(f'Waiting for add business view link and count divs placeholders')

            # при достижении датафрэйма заданной длины записываем в эксель
            if len(df) >= 10:
                create_append_df_to_excel(filename=RESULT_FILE, df=df,)
                df = pd.DataFrame(columns=['Название', 'Адрес', 'Контакты', 'Сайт', 'Соц сети', 'Ссылка', 'Координаты',])
                logger.info("10 rows is writed - %s", )
        if len(df) != 0:
            create_append_df_to_excel(filename=RESULT_FILE, df=df, )
            logger.info("%s rows wrote ", len(df))
        print('page_crawl is done')
    except Exception as exc:
        logger.exception("PAGE_CROWLER IS full DOWN: %s ", url, exc)
    finally:
        driver.close()
        driver.quit()


def get_data(driver, card):
    global COUNT
    global MAX_COUNT
    result = {}
    result['Название'] = get_name_company(driver, logger, card)
    result['Адрес'] = get_addresses(driver, logger, card)
    result['Контакты'] = get_contacts(driver, logger, card)
    result['Сайт'] = get_site(driver, logger, card)
    result['Соц сети'] = get_soc_network(driver, logger, card)
    result['Ссылка'] = cur_url(driver, logger, card)
    result['Координаты'] = get_coordinates(driver, logger, card)
    logger.info("[+][+][+][+]  Processed:  %s / %s   [+][+][+][+]", COUNT, MAX_COUNT)
    return result


@time_track
def main():
    global COUNT
    global MAX_COUNT
    ### Открываем файл запросов и сохраяем в список
    logger.info("Open file requests %s", FILE_REQUESTS)
    with open(FILE_REQUESTS, encoding='utf-8') as file:
        requests_list = []
        for item in file.readlines():
            requests_list.append(item.strip())
    logger.info("file requests is opened, his len is %s", len(requests_list))

    # в файле request.txt находятся запросы в поисковик яндекс карт
    # в CITIES находится список городов - перебираем все запросы по городам
    for reque in requests_list:
        for city in CITIES:
            my_url = f'https://yandex.by/maps/?text={reque}+{city}'
            logger.info("cicle of FOR for next values reque - %s city - %s  current url - %s", reque, city, my_url)
            page_crawl(url=my_url)
            if COUNT >= MAX_COUNT:
                break
        if COUNT >= MAX_COUNT:
            break


if __name__ =='__main__':
    main()