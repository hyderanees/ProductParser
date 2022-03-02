from bs4 import BeautifulSoup
import os
from selenium import webdriver

BASE_URL = "https://www.distrizone.ro/inregistrare"
USERNAME = "klf118@yahoo.com"
PASSWORD = "Jk36puW8KAJzhN6"
CHROME_NAME = "chromedriver"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'sitesparser', CHROME_NAME)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# DRIVER_PATH = PATH
DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'


def login_to_website(driver):
    driver.set_page_load_timeout(15)
    driver.get(BASE_URL)
    username = driver.find_element_by_id("_loginEmail")
    password = driver.find_element_by_id("_loginPassword")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    driver.implicitly_wait(10)

    a_elements = driver.find_element_by_id('doLogin')
    a_elements.submit()
    return


def get_detail_of_url_page(url, driver):
    driver.set_page_load_timeout(15)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


def get_stock_value(soup):
    try:
        stock_ = soup.find('span', {'class': 'stock-status'})
        stock_ = stock_.text.strip()

        if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand' \
                or stock_.lower() == 'lack of stock' or stock_.lower() == 'out-of-stock':
            stock_ = 'no stock'
        elif stock_.lower() == 'in stoc' or stock_.lower() == 'in stock':
            stock_ = 'in stock'
        else:
            stock_ = 'N/A'
    except:
        stock_ = 'N/A'
    return stock_


class DistriZoneInformation:

    def __init__(self, finding_url):
        self.finding_url = finding_url

    def get_prices(self):
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        try:
            login_to_website(driver)
            soup = get_detail_of_url_page(self.finding_url, driver)
            original_price = soup.find_all('input', {'id': 'productBasePrice'})
            promotion_price = soup.find_all('input', {'id': 'productFinalPrice'})
            original_price = original_price[0].attrs['value']
            promotion_price = promotion_price[0].attrs['value']

            original_price = float(original_price)
            promotion_price = float(promotion_price)

            stock = get_stock_value(soup)

        except Exception as e:
            print(e)
            driver.close()
            return False

        driver.close()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.finding_url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


# url = "https://www.distrizone.ro/iiphone-5s/ecran-iphone-5s-negru.html"
# DistriZoneInformation(url)
