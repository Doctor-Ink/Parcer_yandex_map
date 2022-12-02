from pprint import pprint

import requests
from bs4 import BeautifulSoup


url = "https://города-россия.рф/reytin-cities.php?name=%D1%81%D1%80%D0%B5%D0%B4%D0%BD%D0%B8%D0%B5"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0"
}

response = requests.get(url=url, headers=headers)

soup = BeautifulSoup(response.content, 'lxml')

list_cities = []
for item in soup.find('ol').find_all('a'):
    list_cities.append(item.get_text())

with open('cities.txt', 'w', encoding='utf-8') as file:
    for item in list_cities:
        file.write(f'{item}\n')

pprint(list_cities)