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
wait = WebDriverWait(driver, 40)


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


def find_year(drvr):
    """
    Finds all "year" class elements on the page
    :param drvr: selenium driver
    :return: year_list list
    """
    year_class_elements = drvr.find_elements(by=By.CLASS_NAME, value="_3eOdkTDYdWyo_U5-JPeer1")
    year_list = []
    for ti in year_class_elements:
        year_list.append(ti.get_attribute("textContent"))
    return year_list


def find_rating(drvr, x):
    """
    Finds all "title" class elements on the page
    :param drvr: selenium driver
    :param x: number of a game in the list
    :return: mark_list list
    """
    mark_class_elements = drvr.find_elements(by=By.XPATH,
                                             value=f'//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]/div[2]'
                                                   f'/div/div[{x}]/div/div/div/div[2]/div[3]/a/div/div[1]')
    mark_list = []
    for ti in mark_class_elements:
        mark_list.append(ti.text)
    return mark_list


def find_price(drvr):
    """
    Finds all "price" class elements on the page
    :param drvr: selenium driver
    :return: price_list list
    """
    price_class_elements = drvr.find_elements(by=By.CLASS_NAME, value="Wh0L8EnwsPV_8VAu8TOYr")
    price_list = []
    for ti in price_class_elements:
        price_list.append(ti.get_attribute("textContent"))
    return price_list


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
    return writer


def next_page_button(drvr):
    """
    Finds a "Показать больше" button by XPATH value //button[contains(text(), \'Показать больше\')]'
    :param drvr: selenium driver
    :return: selenium element or None
    """
    wait.until(EC.presence_of_element_located((By.XPATH, f'//button[contains(text(), \'Показать больше\')]')))
    button_class_element = drvr.find_element(by=By.XPATH, value=f'//button[contains(text(), \'Показать больше\')]')
    if "Показать больше" in button_class_element.text:
        print('Button is founded')
        return button_class_element
    print('Button is missing')
    return None


if __name__ == '__main__':
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 25000);")
    time.sleep(15)
    titles_list = []
    number_pages = 0

    while number_pages < 6:
        print('number_pages:', number_pages)
        # get Next Page button element
        button = next_page_button(driver)
        # check if it is the last page
        if button is None:
            break
        # go to next page
        button.click()
        print('click')
        driver.execute_script("window.scrollTo(0, 15000);")
        time.sleep(15)
        number_pages += 1

    # get parameters lists
    titles_list = find_title(driver)
    years_list = find_year(driver)
    prices_list = find_price(driver)
    rating_list = [driver.find_element(by=By.XPATH,
                                       value=f'//*[@id="SaleSection_13268"]/div[2]/div[2]/div[2]'
                                             f'/div[2]/div/div[{num}]/div/div/div/div[2]/div[3]/a/div/div[1]').text
                   for num in range(1, len(titles_list) + 1)]
    # make csv file  with parameters
    data = dict_to_csv()
    # closing the driver
    driver.quit()
