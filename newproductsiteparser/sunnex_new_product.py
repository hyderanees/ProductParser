from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://sunex.ro/nou/produse-noi"
LOGIN_BASE_URL = "https://sunex.ro"
USERNAME = "itool_service@yahoo.com"
PASSWORD = "samsung22"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


class SunnexInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.pagination_info = 0
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def login_to_website(self):
        self.driver.get(LOGIN_BASE_URL)
        self.driver.implicitly_wait(10)
        username = self.driver.find_element_by_id("email")
        password = self.driver.find_element_by_id("passwd")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        self.driver.find_element_by_id("SubmitLogin").click()
        return

    def get_products_page(self):
        self.login_to_website()
        self.driver.get(BASE_URL)
        self.driver.implicitly_wait(10)
        self.get_pagination_information()
        self.iterate_over_product_pagination()

        for obj in range(2, self.pagination_info):
            url = BASE_URL + '?page=' + str(obj)
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            self.iterate_over_product_pagination()
        self.driver.close()

    def iterate_over_product_pagination(self):
        self.get_every_page_detail_with_soup()

    def get_every_page_detail_with_soup(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        products = soup.find('div', {'id': 'js-product-list'})
        if products:
            data_obj = products.find_all('div', {'class': 'item'})
            for obj in data_obj:
                try:
                    self.get_detail_of_single_product_with_soup(obj)
                except Exception as e:
                    pass

    def get_detail_of_single_product_with_soup(self, data_obj):
        href_img = data_obj.find('div', {'class': 'left-product'})
        href_link = href_img.find('a').attrs['href']
        img_tag = href_img.find('img').attrs['src']

        title_price_ = data_obj.find('div', {'class': 'right-product'})
        title_ = title_price_.find('div', {'class': 'product_name'})
        title_ = title_.find('a').text

        price_ = title_price_.find('span', {'class': 'price'}).text
        price_ = price_.strip()
        price_ = price_.replace('\xa0', '')

        original_price = price_
        promotional_price = price_

        dict_ = {
            'title': title_.strip(),
            'original_price': original_price.strip(),
            'promotional_price': promotional_price.strip(),
            'href_link': href_link.strip(),
            'img_tag': img_tag
        }
        self.resultant_list.append(dict_)

    def get_pagination_information(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        pagination_info = soup.find('ul', {'class': 'page-list'})
        pagination_info = pagination_info.find_all('li')

        list_param = []
        for obj in pagination_info:
            id_ = obj.text.strip()
            try:
                id_ = int(id_)
                list_param.append(id_)
            except:
                pass

        list_param = max(list_param)
        self.pagination_info = list_param


# pin = SunnexInformationNewProducts()
# pin.get_products_page()
# print(len(pin.resultant_list))
# print(pin.resultant_list)
