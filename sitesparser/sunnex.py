from bs4 import BeautifulSoup
import os
from selenium import webdriver
import time

BASE_URL = "https://sunex.ro"
USERNAME = "itool_service@yahoo.com"
PASSWORD = "samsung22"
CHROME_NAME = "chromedriver"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE_DIR, 'sitesparser', CHROME_NAME)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

DRIVER_PATH = PATH
DRIVER_PATH = '/usr/bin/chromedriver'


def login_to_website(driver):
    driver.set_page_load_timeout(15)
    driver.get(BASE_URL)
    time.sleep(3)
    username = driver.find_element_by_id("email")
    password = driver.find_element_by_id("passwd")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    driver.find_element_by_id("SubmitLogin").click()
    return


def get_detail_of_url_page(url, driver):
    driver.set_page_load_timeout(15)
    driver.get(url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "lxml")
    return soup


def SunnexMobile(finding_url):
    stock = 'N/A'

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
    try:
        login_to_website(driver)
        soup = get_detail_of_url_page(finding_url, driver)
        product_info = soup.find_all('div', class_="product-prices")[0]
        original_price = product_info.find('div', class_="current-price")

        original_price = original_price.find('span').text
        original_price = original_price.replace(',', '.')
        original_price = original_price.replace('RON', '')

        original_price = float(original_price)
        promotion_price = original_price
    except Exception as e:
        print (e)
        driver.close()
        return False

    driver.close()

    print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
    return {'url': finding_url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


# finding_url = "https://sunex.ro/nou/module-incarcare-flex-uri-mufa-incarcare/8611-modul-incarcare-apple-iPhone-5-alb.html"
# SunnexMobile(finding_url)