import requests
from bs4 import BeautifulSoup

url = 'https://yandex.com.am/weather/'
response = requests.get(url)
print(response)

bs = BeautifulSoup(response.text, "lxml")
temp = bs.find('span', 'temp__value temp__value_with-unit')
print(temp)
if temp:
    print(f'Температура: {temp.text} градусов Цельсия')
else:
    print("Тег <span> не найден.")
