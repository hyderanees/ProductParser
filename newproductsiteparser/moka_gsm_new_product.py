import time

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://www.moka-gsm.ro/{}?o=news"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

CATEGORIES = ['accesorii', 'reparatii', 'telefoane-mobile', 'pc-periferice-software',
              'piese-si-componente-gsm', 'trotinete-electrice', 'piese-electrocasnice',
              'outdoor', 'cantar-smart', 'accesorii-offroad', 'adezivi-si-agenti-de-curatare',
              'aparatura-service', 'aspiratoare', 'banda-led', 'cartele-gsm', 'credite',
              'echipamente-de-protectie', 'ingrijire-corp', 'smart-home', 'smartwatch']
# CATEGORIES = ['telefoane-mobile']


class MokaGSMInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.pagination_info = 0
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def get_products_page(self):
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
        soup = soup.find('div', {'class': 'product-listing'})
        if soup:
            data_obj = soup.find_all('div', {'class': 'product-box'})
            for obj in data_obj:
                try:
                    self.get_detail_of_single_product_with_soup(obj)
                except Exception as e:
                    pass

    def get_detail_of_single_product_with_soup(self, data_obj):
        image_holder = data_obj.find('div', {'class': 'image-holder'})
        href_link_ = image_holder.find('a').attrs['href']

        is_new_tag_available = False
        properties_check = image_holder.find('div', {'class': 'product-icon-box'})
        new_tag_check = properties_check.find_all('span', {'class': 'new'})
        if new_tag_check:
            is_new_tag_available = True

        if not is_new_tag_available:
            return

        img_tag = image_holder.find('img')
        if img_tag:
            img_tag = img_tag.attrs['src']
        else:
            img_tag = ''

        title_price = data_obj.find('div', {'class': 'top-side-box'})
        title_ = title_price.find('h2').text
        price_ = title_price.find('div', {'class': 'price'})

        promotional_check = price_.find_all('s', {'class': 'price-full'})
        original_check = price_.find('span', {'class': 'text-main'}).text

        if promotional_check:
            promotional_check = promotional_check[0].text
        else:
            promotional_check = original_check

        original_price = original_check.replace('\xa0', '')
        promotional_price = promotional_check.replace('\xa0', '')

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


# mgs = MokaGSMInformationNewProducts()
# mgs.get_products_page()
# print(mgs.resultant_list)
