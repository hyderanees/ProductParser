from bs4 import BeautifulSoup
import os
from selenium import webdriver

CHROME_NAME = "chromedriver"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'sitesparser', CHROME_NAME)

DRIVER_PATH = '/usr/bin/chromedriver'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def login_to_website(driver):
    driver.get("https://www.magazingsm.ro/")
    return


def get_detail_of_url_page(url, driver):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def SEPMobileMainFunction(finding_url):
    stock = 'N/A'

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
    try:
        login_to_website(driver)
        soup = get_detail_of_url_page(finding_url, driver)
        # promotion_price = soup.find('span', class_="eroare").text

        price_obj = soup.find('div', {'class': 'price-box'})
        original_price = price_obj.find('p', {'class': 'regular-price'})

        if original_price:
            original_price = original_price.find('span', {'class': 'price'}).text.replace('Lei', '')
            promotion_price = original_price
        else:
            promotion_price = price_obj.find('p', {'class': 'special-price'})
            original_price = price_obj.find('p', {'class': 'old-price'})
            promotion_price = promotion_price.find('span', {'class': 'price'}).text.replace('Lei', '')
            original_price = original_price.find('span', {'class': 'price'}).text.replace('Lei', '')

    except Exception as e:
        print (e)
        driver.close()
        return False

    driver.close()

    print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
    return {'url': finding_url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


finding_url = "https://www.magazingsm.ro/piese-telefon/folie-sticla-iphone-6-iphone-6s-50184"
SEPMobileMainFunction(finding_url)
