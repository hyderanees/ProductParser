import os
from selenium import webdriver
from bs4 import BeautifulSoup

CHROME_NAME = "chromedriver"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'sitesparser', CHROME_NAME)

# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
DRIVER_PATH = '/usr/bin/chromedriver'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def get_detail_of_url_page(url, driver):
    driver.set_page_load_timeout(15)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def get_stock_value(soup):
    try:
        stock_ = soup.find('div', {'class': 'stock'})
        stock_ = stock_.contents[0]

        if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand' \
                or stock_.lower() == 'lack of stock' or stock_.lower() == 'out-of-stock' or stock_.lower() == ''\
                or stock_.lower() == 'Disponibilitate: nu este in stoc':
            stock_ = 'no stock'
        elif stock_ == 'Disponibilitate: in stoc':
            stock_ = 'in stock'
        else:
            stock_ = 'N/A'
    except:
        stock_ = 'N/A'
    return stock_


class TradeGSMInformation():
    def __init__(self, finding_url):
        self.url = finding_url

    def get_prices(self):
        stock = 'N/A'

        driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        try:
            soup = get_detail_of_url_page(self.url, driver)
            # promotion_price = soup.find('span', class_="eroare").text

            price_obj = soup.find('div', {'id': 'product_price'})
            original_price = price_obj.contents[0]
            promotion_price = original_price

            original_price = original_price.replace('.', '')
            promotion_price = promotion_price.replace('.', '')

            original_price = float(original_price)
            promotion_price = float(promotion_price)
            stock = get_stock_value(soup)
        except Exception as e:
            print(e)
            driver.close()
            return False

        driver.close()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price,
                'stock': stock}


# url = "https://www.tradegsm.ro/display/lcd-display-cu-touchscreen-huawei-p30-lite-negru-mar-l01a-mar-l21a-mar-lx1a-europe-mar-lx1m-1222.html"
# TradeGSMInformation(url).get_prices()
