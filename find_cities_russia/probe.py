
list_cities = []
with open('cities.txt', encoding='utf-8') as file:
    reader = file.read()
    for line in reader.split('\n'):
        list_cities.append(line)
    list_cities = list_cities[:-1]
print(list_cities[51:52])