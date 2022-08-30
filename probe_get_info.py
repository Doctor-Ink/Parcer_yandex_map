import time
from pprint import pprint
from random import choice
import requests
from bs4 import BeautifulSoup

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
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36', # из браузера Chrome
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0', # из браузера Mozila
]

headers = {
    "user-agent": f"{choice(user_agents_list_desktop)}",
    # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",   # из браузера Chrome
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",   # из браузера Мозила
    "accept-encoding": "gzip, deflate, br",
    # "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    # "method": "GET",
    # "Content-Type": "application/json",
    # "referer": "https://yandex.by/maps/org/tsentralnaya_rayonnaya_poliklinika_14/1117695633/?ll=27.610286%2C53.904231&z=16",
}

print(headers)
url = 'https://yandex.by/maps/org/tsentralnaya_rayonnaya_poliklinika_14/1117695633/'
url1 = 'https://yandex.by/maps/org/tsentralnaya_rayonnaya_poliklinika_14/1117695633/?ll=27.610286%2C53.904231&z=16'
url2 = 'http://httpbin.org/get'

# # генерим рандомные юзер агенты
# desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
#                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
#                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
#                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
# def random_headers():
#     return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
# r = requests.get(url=url,headers=random_headers())
# print(r)


# редиректы
# response_with_redirect = requests.get(url=url, headers=headers)
# print(response_with_redirect.url)
# print(response_with_redirect.status_code)
# print(response_with_redirect.history)
# print(response_with_redirect.text)


responce = requests.get(url=url, headers=headers, timeout=10)
time.sleep(1)
print(responce)
# pprint(responce.headers)
# print(responce.text)
soup = BeautifulSoup(responce.text, 'lxml')

try:
    print(soup.find('h1', {'class': 'orgpage-header-view__header'}))
    item_name = soup.find('h1', {'class': 'orgpage-header-view__header'}).text.strip()
except Exception as exc:
    item_name = None

try:
    item_phone = soup.find('div', class_='card-phones-view__phone-number').text.strip()
except Exception as exc:
    item_phone = None

print(item_name, item_phone)