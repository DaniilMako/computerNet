from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# site = "https://www.cifrus.ru/"


def parser(site):
    browser = webdriver.Firefox()
    browser.maximize_window()
    browser.implicitly_wait(5)
    browser.get(site)

    # what you whant to search
    product_search = "Беспроводные наушники"
    # print(product_search)

    # write to "search" form and search
    browser.find_element(By.XPATH, "//input[@type='text']").send_keys(product_search)
    browser.find_element(By.XPATH, "//button[@type='submit']").click()
    print('поиск')

    # go to detailed mode
    browser.find_element(By.XPATH, "//button[@id='list-view']").click()
    print("поиск завершился")

    class_name = ".product-layout.product-list.col-xs-12"
    products = browser.find_elements(By.CSS_SELECTOR, class_name)
    # print('products:', products)

    with open(f"cifrus_{product_search}.csv", "w", encoding="utf-16", newline='') as file:
        writer = csv.writer(file, quotechar=";", delimiter=";")
        writer.writerow(['id', 'name', 'url', 'characteristics', 'price'])
        print('parser begin')
        for number, product in enumerate(products):
            # get name and url
            name_url = product.find_element(By.XPATH, ".//div/div[3]/div[1]/a")
            name = name_url.text

            url = name_url.get_attribute("href")
            # print('name:', name, 'url:', url)

            # get characteristics
            characteristics = product.find_elements(By.XPATH, ".//div/div/div[3]/div[3]/table/tbody/tr")
            full_characteristic = []
            # print('\ncharacteristics got:', len(characteristics))
            for characteristic in characteristics:
                full_characteristic.append(characteristic.text)

            # get price
            price = product.find_element(By.XPATH, ".//div/div[3]/div[4]").text

            # write to file
            info = [str(number + 1), name, url, full_characteristic, price]
            # print(info)
            # file.write(info)
            writer.writerow(info)

    browser.close()
    return (f"cifrus_{product_search}.csv")

# parser(site)
