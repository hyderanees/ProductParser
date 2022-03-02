import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://www.distrizone.ro/{}?o=news"
LOGIN_URL = "https://www.distrizone.ro/inregistrare"
USERNAME = "klf118@yahoo.com"
PASSWORD = "Jk36puW8KAJzhN6"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

CATEGORIES = ['accesorii', 'acumulatori-huawei', 'acumulatori-iphone', 'acumulatori-samsung',
              'capace-spate-service-pack', 'capace-spate-swap', 'ecrane-samsung-seria-a',
              'ecrane-samsung-seria-j', 'ecrane-samsung-m', 'ecrane-samsung-seria-n',
              'ecrane-samsung-seria-s', 'ecrane-huawei', 'ecrane-huawei-service-pack',
              'ecrane-honor', 'ecrane-iphone', 'ecrane-motorola', 'ecrane-nokia', 'ecrane-oppo',
              'ecrane-oneplus', 'ecrane-xiaomi', 'ecrane-tablete', 'flex-incarcare-samsung']
# CATEGORIES = ['ecrane-xiaomi']


class DistrizoneInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.pagination_info = 0
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def login_to_website(self):
        self.driver.get(LOGIN_URL)
        self.driver.implicitly_wait(10)
        username = self.driver.find_element_by_id("_loginEmail")
        password = self.driver.find_element_by_id("_loginPassword")
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        self.driver.implicitly_wait(10)
        a_elements = self.driver.find_element_by_id('doLogin')
        a_elements.submit()
        return

    def get_products_page(self):
        self.login_to_website()
        for obj in CATEGORIES:
            url = BASE_URL.format(obj)
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            # self.get_pagination_information()
            self.iterate_over_product_pagination(obj)
        self.driver.close()

    def iterate_over_product_pagination(self, category):
        self.get_every_page_detail_with_soup()
        # counter = 1
        # if self.pagination_info:
        #     for obj in range(self.pagination_info - 1):
        #         counter += 1
        #         self.driver.get(BASE_URL.format(category, counter))
        #         self.get_every_page_detail_with_soup()

    def get_every_page_detail_with_soup(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        products = soup.find('div', {'class': 'product'})
        if products:
            data_obj = products.find_all('div', {'class': 'product-box'})
            for obj in data_obj:
                try:
                    self.get_detail_of_single_product_with_soup(obj)
                except Exception as e:
                    pass

    def get_detail_of_single_product_with_soup(self, data_obj):
        data_obj = data_obj.find('div', {'class': 'box-holder'})
        href_img = data_obj.find('div', {'class': 'image-holder'})

        href_link = href_img.find('a')
        href_link_ = href_link.attrs['href']
        img_tag = href_img.find('img')
        if img_tag:
            img_tag = img_tag.attrs['src']
        else:
            img_tag = ''

        tag_finder = href_img.find('div', {'class': 'product-icon-box'})
        is_new_ = tag_finder.find('span', {'class': 'new'})
        if not is_new_:
            return

        title_price_ = data_obj.find('div', {'class': 'top-side-box'})
        title_ = title_price_.find('h2').text

        price_ = title_price_.find('div', {'class': 'price'})
        if not price_:
            return

        price = price_.find('span', {'class': 'text-main'})
        any_promotional_check_price = price_.find('s', {'class': 'price-full'})

        if not price:
            return

        if any_promotional_check_price:
            promotional_price = any_promotional_check_price.text
            original_price = price.text
            if not promotional_price:
                promotional_price = original_price
        else:
            promotional_price = price.text
            original_price = price.text

        original_price = original_price.replace('\xa0', '')
        promotional_price = promotional_price.replace('\xa0', '')

        dict_ = {
            'title': title_.strip(),
            'original_price': original_price.strip(),
            'promotional_price': promotional_price.strip(),
            'href_link': href_link_.strip(),
            'img_tag': img_tag
        }
        self.resultant_list.append(dict_)

    def get_pagination_information(self):
        data_obj_ = self.driver.find_elements_by_class_name('woocommerce-pagination')
        if data_obj_:
            self.pagination_info = data_obj_[0].find_element_by_tag_name('ul')
            self.pagination_info = self.pagination_info.find_elements_by_tag_name('li')
            self.pagination_info = int(self.pagination_info[-2].text)
            self.driver.implicitly_wait(10)
        else:
            self.pagination_info = 0


# pin = DistrizoneInformationNewProducts()
# pin.get_products_page()
# print(len(pin.resultant_list))
# print(pin.resultant_list)
