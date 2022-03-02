import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://servicepack.ro/categorie-produs/{}page/{}/?orderby=date"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

CATEGORIES = ['samsung/', 'huawei/', 'iphone/', 'xiaomi/', 'componente/baterii/', 'piese/']
# CATEGORIES = ['xiaomi/']


class ServicePackInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.pagination_info = 0
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def get_products_page(self):
        for obj in CATEGORIES:
            url = BASE_URL.format(obj, 1)
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            self.get_pagination_information()
            self.iterate_over_product_pagination(obj)
        self.driver.close()

    def iterate_over_product_pagination(self, category):
        self.get_every_page_detail_with_soup()
        counter = 1
        if self.pagination_info:
            for obj in range(self.pagination_info - 1):
                counter += 1
                self.driver.get(BASE_URL.format(category, counter))
                self.get_every_page_detail_with_soup()

    def get_every_page_detail_with_soup(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        soup = soup.find('div', {'class': 'main-content'})
        products = soup.find('ul', {'class': 'products'})
        if products:
            data_obj = products.find_all('li')
            for obj in data_obj:
                try:
                    self.get_detail_of_single_product_with_soup(obj)
                except Exception as e:
                    pass

    def get_detail_of_single_product_with_soup(self, data_obj):
        href_link = data_obj.find_all('a')
        href_link_ = href_link[0].attrs['href']
        title_ = href_link[1].find('h2').text
        price_ = data_obj.find('span', {'class': 'price'}).text
        price_ = price_.replace('\xa0', '')

        img_tag = href_link[0].find('img')
        if img_tag:
            img_tag = img_tag.attrs['src']
        else:
            img_tag = ''

        original_price = price_
        promotional_price = price_

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


# spi = ServicePackInformationNewProducts()
# spi.get_products_page()
# print(spi.resultant_list)
