import undetected_chromedriver as uc


driver = uc.Chrome()
try:
    driver.get(url="https://yandex.by/maps/org/banya/212564828178/")
    driver.maximize_window()

    current_url = driver.current_url
    print(current_url)
    # https://yandex.by/maps/org/banya_na_kurskoy/232229006327/?ll=35.432039%2C52.331216&z=9
    some_list = current_url.split('/')[-1].split('.')
    coordinates = [some_list[0][-2:] + '.' + some_list[1][:6] + ', ' + some_list[1][-2:] + '.' + some_list[2][:6]]
    print(coordinates)
except Exception as exc:
    print(exc)
# my_url = 'https://yandex.by/maps/org/banya_na_kurskoy/232229006327/?ll=35.432039%2C52.331216&z=9'
# my_url = 'https://yandex.by/maps/org/gorodskaya_banya/105723579482/?ll=35.368434%2C52.329408&z=16'
# [55.79269608848491,37.65145873767102]


# some_list = my_url.split('/')[-1].split('.')
# coordinates = [some_list[0][-2:] + '.' + some_list[1][:6] + ', ' + some_list[1][-2:] + '.' + some_list[2][:6]]
# print(coordinates)