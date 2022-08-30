import re
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains


service = Service('C:\\Users\\Zver\\PycharmProjects\\Parcers\\web_content\\chromedriver\\chromedriver_win32\\chromedriver.exe')
url = 'https://www.divan.ru/perm/product/alfa-milk-puf'



# try:
#     driver.get(url=url)
#     driver.maximize_window()
#     # 'div', class_='result-card'
#     time.sleep(9)
#     div_all = driver.find_element(By.CSS_SELECTOR, '.result-card_arrow')
#     div_all.click()
#     time.sleep(6)
#     print(driver.current_url)
#     print(div_all)
# except Exception as exc:
#     print(exc)
# finally:
#     driver.close()
#     driver.quit()
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get(url)
    divs_all = driver.find_elements(By.CLASS_NAME, 'xjyjk HWvH3 VipTl')
    pprint(divs_all)
    img_list = []
    for elem in divs_all:
        cur_url = re.search(r'https:*.jpg', elem.get_attribute('style')).group()
        if cur_url not in img_list:
            print(cur_url)
            img_list.append(cur_url)
except Exception as exc:
    print(exc)
finally:
    driver.close()
    driver.quit()