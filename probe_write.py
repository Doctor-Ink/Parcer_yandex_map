import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.relative_locator import locate_with

def get_source_html(url):

    options = webdriver.ChromeOptions()
    ##### user-agent ########
    user_agents_list_mobile = [
        'Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1',
        'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536',
    ]
    user_agents_list_desktop = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    ]
    # options.add_argument(f"user-agent={random.choice(user_agents_list_desktop)}")

    # disable wevdriver mode
    options.add_argument("--disable-blink-features=AutomationControlled")

    # версия драйвера Index of /104.0.5112.20/
    service = Service(
        'C:\\Users\\Zver\\PycharmProjects\\parcer_get_map_polyclinic\\chromedriver\\chromedriver_win32\\chromedriver.exe',
    )
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    try:
        # open url
        driver.get(url)
        time.sleep(1)
        driver.implicitly_wait(30)
        with open("probe_page.html", mode='w', encoding='utf-8') as file:
            file.write(driver.page_source)
    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()


def main():
    get_source_html(url='https://yandex.by/maps/157/minsk/search/%D0%BF%D0%BE%D0%BB%D0%B8%D0%BA%D0%BB%D0%B8%D0%BD%D0%B8%D0%BA%D0%B0%20%D0%BC%D0%B8%D0%BD%D1%81%D0%BA/?ll=27.603947%2C53.900782&sctx=ZAAAAAgCEAAaKAoSCUxTBDi9jztAEapiKv2E80pAEhIJnZ53Y0Fh0z8RH9sy4Cwluz8iBgABAgMEBSgKOABAnQFIAWI0cmVsZXZfcmFua2luZ19oZWF2eV9jbGlja19tYXBzX2Zvcm11bGE9MC4yOmZtbDg2ODQ5MmI1cmVsZXZfcmFua2luZ19oZWF2eV9yZWxldl9tYXBzX2Zvcm11bGE9MC44OmwzX2RjNjY4ODRqAnVhnQHNzEw9oAEAqAEAvQHFYBI9wgGBAYyvx%2BcD8raf7QO%2FicP%2BA5Hd%2BpQEoZXhpATImOKXBPmj8owFgpGHkQSPhveABJmmzPKXA9LxyuMD25fjiQTBrJ3xA%2Bjr7%2FcDuveNsfUEvK%2BvhASdzIvFBNLs4oIEn6%2Fa6wONx%2B%2B%2FBPerqI4Ewf%2B6%2BAPRn72NBObonfjpA8Hj4In0AeoBAPIBAPgBAIICIdC%2F0L7Qu9C40LrQu9C40L3QuNC60LAg0LzQuNC90YHQuooCEzE4NDEwNjAxNCQxODQxMDU5ODaSAgMxNTeaAgxkZXNrdG9wLW1hcHM%3D&sll=27.603947%2C53.900782&sspn=0.347838%2C0.121804&z=11.8')
    # get_source_html(url='https://www.whatismybrowser.com/')        # узнать под каким браузером имитация работы
    # get_source_html(url='https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')  # узнать, видна ли работа драйвера


if __name__ =='__main__':
    main()




