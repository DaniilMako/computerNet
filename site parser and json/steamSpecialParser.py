from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import json
import time


def find_by_css_selector(drvr, value):
    class_elements = drvr.find_elements(By.CSS_SELECTOR, value)
    list = []
    for ti in class_elements:
        list.append(ti.get_attribute("textContent"))
    return list


def find_by_class_name(drvr, value):
    class_elements = drvr.find_elements(by=By.CLASS_NAME, value=value)
    list = []
    for ti in class_elements:
        list.append(ti.get_attribute("textContent"))
    return list


def dict_to_csv(titles_list, years_list, rating_list, prices_list, filename='steamSpecials.csv'):
    """
    Saves a dictionary with ['title', 'year', 'rating', 'price'] columns (title, year, rating, price)
    :param filename: str, name of file where to save
    :return: Nothing
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar=";", delimiter=";")
        writer.writerow(['title', 'year', 'rating', 'price'])
        for i in range(len(titles_list)):
            writer.writerow([titles_list[i], years_list[i], rating_list[i], prices_list[i]])

    return writer.name


def start(url):
    # url = 'https://store.steampowered.com/specials'
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 50)

    driver.get(url)
    driver.execute_script("window.scrollTo(0, 1500);")
    time.sleep(5)
    number_pages = 0

    for i in range(3):
        # Find the button with class name `_3d9cKhzXJMPBYzFkB_IaRp Focusable`
        print(f'number page: {i}')
        button_element = None
        while button_element is None:
            try:
                # scroll down the page by 300 pixels
                driver.execute_script("window.scrollBy(0, 300);")
                button_element = driver.find_element(By.CSS_SELECTOR, 'button._3d9cKhzXJMPBYzFkB_IaRp.Focusable')
                button_element.click()
            except:
                time.sleep(2)  # wait for 1 second before scrolling again
    # get parameters lists
    print('start writing parameters\n')
    titles_list = find_by_class_name(driver, "_1F4bcsKc9FjeWQ2TX8CWDe")
    years_list = find_by_class_name(driver, "_3eOdkTDYdWyo_U5-JPeer1")[:len(titles_list)]
    prices_list = find_by_css_selector(driver,
                                       "div._1gO7r6Xr5gQHoBBkERY0gd div._3GLeQSpjtTPdHW4J8KwCSa div.Wh0L8EnwsPV_8VAu8TOYr")[
                  :len(titles_list)]
    rating_list = find_by_css_selector(driver,
                                       'div._2wLns48qa0uwOUf7ktqdsC div._2SbZztpb7hkhurwbFMdyhL > div:first-child')[
                  :len(titles_list)]

    print('titles_list:', len(titles_list))
    print('years_list: ', len(years_list))
    print('rating_list:', len(rating_list))
    print('prices_list:', len(prices_list))

    # closing the driver
    driver.quit()

    data_list = dict_to_csv(titles_list, years_list, rating_list, prices_list)
    return data_list


# if __name__ == '__main__':
#     start('https://store.steampowered.com/specials')
