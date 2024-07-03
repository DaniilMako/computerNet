import csv

from selenium import webdriver
from selenium.webdriver.common.by import By


def init_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Edge(options=options)
    return driver


def save_doc(items):
    path = 'web_parser_result.csv'
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Brand', 'Price', 'Title', 'Href'])
        for item in items:
            writer.writerow([item['brand'], item['price'], item['title'], item['href']])
    return 0


def find_attributes(driver):
    res = []
    for page in range(1, 6):
        url = 'https://www.mosigra.ru/nastolnye-igry/'
        if page != 1:
            url = f"{url}?page={page}"
        driver.get(url)
        content = driver.find_element(By.CLASS_NAME, "products-content")
        container = content.find_element(By.CLASS_NAME, "products-container ")
        items = container.find_elements(By.CLASS_NAME, "card   ")
        for item in items:
            res.append({
                'brand': item.get_attribute("data-brand"),
                'price': item.get_attribute("data-price"),
                'title': item.find_element(By.CLASS_NAME, "card__body").find_element(By.TAG_NAME, "a").
                get_attribute("title"),
                'href': item.find_element(By.CLASS_NAME, "card__body").find_element(By.TAG_NAME, "a").
                get_attribute("href")
            })
        print(res.__len__())
    return res


if __name__ == '__main__':
    with init_driver() as driver:
        result = find_attributes(driver)
        save_doc(result)
