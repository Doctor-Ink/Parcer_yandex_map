import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = uc.Chrome()
wait = WebDriverWait(driver, 5)

try:
    driver.get(url="https://yandex.by/maps/org/russkaya_banya/1337005701/?ll=38.428284%2C52.608706&z=13")
    driver.maximize_window()

    try:
        # ожидаем пока не появится "показать телефон"
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, 'card-phones-view__more'))
        )
        # нажимаем показать телефон
        if driver.find_elements(By.CLASS_NAME, 'card-phones-view__more') != []:
            print('Number 1')
            for item in driver.find_elements(By.CLASS_NAME, 'card-phones-view__more'):
                item.click()
            print('Number 2')
            time.sleep(10)
    except Exception as exc:
        print('Телефон не указан')

    phones_company_list = []

    try:
        phones_company = driver.find_elements(By.CLASS_NAME, 'card-phones-view__phone-number')
        for phone_number in phones_company:
            phone_company = phone_number.text.strip()
            phones_company_list.append(phone_company)
        print('Phone numbers is done!!!')
    except Exception:
        print('Телефон не указан на сайте')
        phones_company_list = None
    print(phones_company_list)


except Exception as exc:
    print(exc)
