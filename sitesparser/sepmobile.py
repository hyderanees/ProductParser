from bs4 import BeautifulSoup
import os

BASE_URL = "https://sepmobile.ro/"
USERNAME = "doctor_gsm"
PASSWORD = "klf118"

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
    driver.set_page_load_timeout(15)
    driver.get(BASE_URL)
    username = driver.find_element_by_id("login_username")
    password = driver.find_element_by_id("login_password")

    username.send_keys(USERNAME)
    password.send_keys(PASSWORD)

    driver.find_element_by_name("submit").click()
    return


def get_detail_of_url_page(url, driver):
    driver.set_page_load_timeout(15)
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
        original_price = soup.find('span', class_="eroare").text

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


# finding_url = "https://sepmobile.ro/accesorii-telefon/breloc-pompon-puf-owl-alte-produse-17304/"
# SEPMobileMainFunction(finding_url)
