import os

from bs4 import BeautifulSoup

BASE_URL = "https://www.magazingsm.ro/"

CHROME_NAME = "chromedriver"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'sitesparser', CHROME_NAME)

# DRIVER_PATH = PATH
DRIVER_PATH = '/usr/bin/chromedriver'
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def login_to_website(driver):
    driver.get(BASE_URL)
    return


def get_detail_of_url_page(url, driver):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def get_stock_value(soup):
    try:
        stock_ = soup.find('p', {'class': 'availability'})
        stock_ = stock_.attrs['class'][1].strip()

        if stock_.lower() == 'out-of-stock':
            stock_ = 'no stock'
        elif stock_.lower() == 'in-stock':
            stock_ = 'in stock'
        else:
            stock_ = 'N/A'
    except:
        stock_ = 'N/A'
    return stock_


class MagaZingSMInformation():
    def __init__(self, finding_url):
        self.url = finding_url

    def get_prices(self):
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

            original_price = original_price.replace(',', '.')
            promotion_price = promotion_price.replace(',', '.')

            original_price = float(original_price)
            promotion_price = float(promotion_price)
            stock = get_stock_value(soup)
        except Exception as e:
            print(e)
            driver.close()
            return False

        driver.close()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': finding_url, 'original_price': original_price, 'promotion_price': promotion_price,
                'stock': stock}


finding_url = "https://www.magazingsm.ro/piese-telefon/acumulator-motorola-moto-z-xt1650-05-original-39025"
MagaZingSMInformation(finding_url).get_prices()
