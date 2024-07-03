from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

url = 'https://store.steampowered.com/specials'
options = webdriver.EdgeOptions()
options.add_argument('--headless')
driver = webdriver.Edge()
wait = WebDriverWait(driver, 50)


def find_rating(drvr):
    """
    Finds all "title" class elements on the page
    :param drvr: selenium driver
    :param x: number of a game in the list
    :return: mark_list list
    """
    year_class_elements = drvr.find_elements(By.CSS_SELECTOR,
                                             'div._2wLns48qa0uwOUf7ktqdsC div._2SbZztpb7hkhurwbFMdyhL > div:first-child')
    mark_list = []
    for ti in year_class_elements:
        mark_list.append(ti.get_attribute('textContent'))
    return mark_list


def find_year(drvr):
    """
    Finds all "year" class elements on the page
    :param drvr: selenium driver
    :return: year_list list
    """
    year_class_elements = drvr.find_elements(By.CLASS_NAME, "_3eOdkTDYdWyo_U5-JPeer1")
    year_list = []
    for ti in year_class_elements:
        year_list.append(ti.get_attribute("textContent"))
    return year_list


def find_price(drvr):
    """
    Finds all "price" class elements on the page
    :param drvr: selenium driver
    :return: price_list list
    """

    price_class_elements = drvr.find_elements(By.CSS_SELECTOR,
                                              'div._1gO7r6Xr5gQHoBBkERY0gd div._3GLeQSpjtTPdHW4J8KwCSa div.Wh0L8EnwsPV_8VAu8TOYr')
    price_list = []
    for ti in price_class_elements:
        price_list.append(ti.get_attribute("textContent"))
    return price_list


def find_title(drvr):
    """
    Finds all "title" class elements on the page
    :param drvr: selenium driver
    :return: title_list list
    """
    title_class_elements = drvr.find_elements(by=By.CLASS_NAME, value="_1F4bcsKc9FjeWQ2TX8CWDe")
    title_list = []
    for ti in title_class_elements:
        title_list.append(ti.get_attribute("textContent"))
    return title_list


def dict_to_csv(filename='steamSpecials.csv'):
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


if __name__ == '__main__':
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 1500);")
    time.sleep(5)
    number_pages = 0

    for i in range(10):
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
    titles_list = find_title(driver)
    years_list = find_year(driver)
    prices_list = find_price(driver)
    rating_list = find_rating(driver)
    print('titles_list:', len(titles_list))
    print('years_list: ', len(years_list))
    print('rating_list:', len(rating_list))
    print('prices_list:', len(prices_list))

    # closing the driver
    driver.quit()

    dict_to_csv()
