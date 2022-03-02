import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://www.magazingsm.ro/noutati/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


class MagaZingSMInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.pagination_info = None
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def get_products_page(self):
        self.driver.get(BASE_URL)
        self.driver.implicitly_wait(10)
        self.change_drop_down_buttons(0)
        self.change_drop_down_buttons(1)
        self.get_pagination_information()
        self.iterate_over_product_pagination()
        self.driver.close()

    def iterate_over_product_pagination(self):
        self.get_every_page_detail_with_soup()
        counter_ = 0
        for obj in range(self.pagination_info - 2):
            counter_ = counter_ + 100
            self.driver.get(BASE_URL + str(counter_))
            self.get_every_page_detail_with_soup()

    def get_every_page_details(self):
        products = self.driver.find_element_by_class_name('product-grid-area')
        data_obj = products.find_element_by_tag_name('ul')
        data_obj = data_obj.find_elements_by_tag_name('li')
        for obj in data_obj:
            self.get_detail_of_single_product(obj)
        self.driver.close()

    def get_every_page_detail_with_soup(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        products = soup.find('div', {'class': 'product-grid-area'})
        data_obj = products.find('ul')
        data_obj = data_obj.find_all('li')
        for obj in data_obj:
            try:
                self.get_detail_of_single_product_with_soup(obj)
            except Exception as e:
                pass

    def get_detail_of_single_product(self, data_obj):
        data_obj = data_obj.find_element_by_class_name('item-inner')
        info_inner = data_obj.find_element_by_class_name('info-inner')
        title_ = info_inner.find_element_by_class_name('item-title')
        href_link_ = title_.find_element_by_tag_name('a').get_attribute("href")
        price_ = data_obj.find_element_by_class_name('item-price')
        img_tag = data_obj.find_elements_by_tag_name('img')
        if img_tag:
            img_tag = img_tag[0].get_attribute('src')
        else:
            img_tag = ''

        special_price_obj = price_.find_elements_by_class_name('special-price')
        old_price_obj = price_.find_elements_by_class_name('old-price')
        regular_price_obj = price_.find_elements_by_class_name('regular-price')

        if special_price_obj and old_price_obj:
            original_price = old_price_obj[0].text
            promotional_price = special_price_obj[0].text
        else:
            original_price = regular_price_obj[0].text
            promotional_price = regular_price_obj[0].text

        original_price = original_price.replace('\xa0', '')
        promotional_price = promotional_price.replace('\xa0', '')

        title_ = title_.text

        dict_ = {
            'title': title_,
            'original_price': original_price,
            'promotional_price': promotional_price,
            'href_link': href_link_,
            'img_tag': img_tag
        }
        self.resultant_list.append(dict_)

    def get_detail_of_single_product_with_soup(self, data_obj):
        data_obj = data_obj.find('div', {'class': 'item-inner'})
        info_inner = data_obj.find('div', {'class': 'info-inner'})

        title_ = info_inner.find('div', {'class': 'item-title'})
        href_link_ = title_.find('a').attrs['href']
        price_ = data_obj.find('div', {'class': 'item-price'})

        img_tag = data_obj.find('img')
        if img_tag:
            img_tag = img_tag.attrs['src']
        else:
            img_tag = ''

        special_price_obj = price_.find_all('p', {'class': 'special-price'})
        old_price_obj = price_.find_all('p', {'class': 'old-price'})
        regular_price_obj = price_.find_all('div', {'class': 'regular-price'})

        if special_price_obj and old_price_obj:
            original_price = old_price_obj[0].find('span', {'class': 'price'}).text
            promotional_price = special_price_obj[0].find('span', {'class': 'price'}).text
        elif special_price_obj or old_price_obj:
            if special_price_obj:
                original_price = special_price_obj[0].find('span', {'class': 'price'}).text
                promotional_price = special_price_obj[0].find('span', {'class': 'price'}).text
            else:
                original_price = old_price_obj[0].find('span', {'class': 'price'}).text
                promotional_price = old_price_obj[0].find('span', {'class': 'price'}).text
        else:
            original_price = regular_price_obj[0].find('span', {'class': 'price'}).text
            promotional_price = regular_price_obj[0].find('span', {'class': 'price'}).text

        title_ = title_.text

        dict_ = {
            'title': title_.strip(),
            'original_price': original_price.strip(),
            'promotional_price': promotional_price.strip(),
            'href_link': href_link_.strip(),
            'img_tag': img_tag
        }
        self.resultant_list.append(dict_)

    def change_drop_down_buttons(self, index_):
        self.data_obj = self.driver.find_element_by_class_name('sorter')
        data_obj_ = self.data_obj.find_elements_by_class_name('short-by')[index_]
        if index_ == 0:
            select = Select(data_obj_.find_element_by_tag_name('select'))
            select.select_by_value('t1___product_id-desc')
        else:
            select = Select(data_obj_.find_element_by_tag_name('select'))
            select.select_by_value('100')
        time.sleep(2)
        self.driver.implicitly_wait(10)

    def get_pagination_information(self):
        data_obj_ = self.driver.find_element_by_class_name('pagination-area')
        self.pagination_info = data_obj_.find_element_by_tag_name('ul')
        self.pagination_info = self.pagination_info.find_elements_by_tag_name('li')
        self.pagination_info = len(self.pagination_info)
        self.driver.implicitly_wait(10)


# mgz = MagaZingSMInformationNewProducts()
# mgz.get_products_page()
# print(mgz.resultant_list)
