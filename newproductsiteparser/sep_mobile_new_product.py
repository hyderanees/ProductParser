from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://sepmobile.ro/accesorii-gsm/noutati/pagina-{}"
LOGIN_BASE_URL = "https://sepmobile.ro/"
USERNAME = "doctor_gsm"
PASSWORD = "klf118"
ADDING_BASE_URL = 'https://sepmobile.ro/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


class SepMobileInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.pagination_info = 0
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def login_to_website(self):
        self.driver.get(BASE_URL)
        self.driver.implicitly_wait(10)
        username = self.driver.find_element_by_id("login_username")
        password = self.driver.find_element_by_id("login_password")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        self.driver.find_element_by_name("submit").click()
        return

    def get_products_page(self):
        self.login_to_website()
        self.driver.get(BASE_URL.format(1))
        self.driver.implicitly_wait(10)
        self.get_pagination_information()
        self.iterate_over_product_pagination()

        for obj in range(2, self.pagination_info):
            url = BASE_URL.format(obj)
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            self.iterate_over_product_pagination()
        self.driver.close()

    def iterate_over_product_pagination(self):
        self.get_every_page_detail_with_soup()

    def get_every_page_detail_with_soup(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        products = soup.find('div', {'class': 'accesorii-gsm-browse'})
        if products:
            data_obj = products.find_all('div', {'class': 'accesoriu-gsm'})
            for obj in data_obj:
                try:
                    self.get_detail_of_single_product_with_soup(obj)
                except Exception as e:
                    print(e)

    def get_detail_of_single_product_with_soup(self, data_obj):
        href_link = data_obj.find('a').attrs['href']
        img_tag = data_obj.find('img').attrs['src']

        title_ = data_obj.find('h2').text
        price_ = data_obj.find('div', {'class': 'pret'})
        price_ = price_.find('span', {'class': 'tag_on'}).text
        price_ = price_.strip()
        price_ = price_.replace('\xa0', '')

        original_price = price_
        promotional_price = price_

        dict_ = {
            'title': title_.strip(),
            'original_price': original_price.strip(),
            'promotional_price': promotional_price.strip(),
            'href_link': ADDING_BASE_URL + href_link.strip(),
            'img_tag': ADDING_BASE_URL + img_tag
        }
        self.resultant_list.append(dict_)

    def get_pagination_information(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        pagination_info = soup.find('div', {'class': 'navbar'})
        pagination_info = pagination_info.find_all('a')

        list_param = []
        for obj in pagination_info:
            try:
                id_ = obj.attrs['href']
                id_ = id_.split('/accesorii-gsm/noutati/pagina-')[1]
                id_ = int(id_)
                list_param.append(id_)
            except:
                pass

        list_param = max(list_param)
        self.pagination_info = list_param


# pin = SepMobileInformationNewProducts()
# pin.get_products_page()
# print(len(pin.resultant_list))
# print(pin.resultant_list)
