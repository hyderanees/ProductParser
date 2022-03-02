from selenium import webdriver
from bs4 import BeautifulSoup

DRIVER_PATH = '/usr/bin/chromedriver'
# DRIVER_PATH = '/home/meharban/Desktop/chromedriver'
BASE_URL = "https://www.gsmnet.ro/produse-noi/page:{}"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


class GsmnetInformationNewProducts:
    def __init__(self):
        self.data_obj = None
        self.maximum_pages_to_visit = 3
        self.is_not_new_product = False
        self.pagination_info = None
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
        self.resultant_list = []

    def get_products_page(self):
        self.driver.get(BASE_URL.format('1'))
        self.driver.implicitly_wait(10)
        self.get_pagination_information()
        self.iterate_over_product_pagination()
        self.driver.close()

    def iterate_over_product_pagination(self):
        self.get_every_page_detail_with_soup()
        counter_ = 1
        for obj in range(self.pagination_info - 2):
            counter_ = counter_ + 1
            if self.is_not_new_product:
                continue
            self.driver.get(BASE_URL.format(counter_))
            self.get_every_page_detail_with_soup()

    def get_every_page_detail_with_soup(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        products = soup.find('div', {'class': 'product-grid-holder'})
        data_obj = products.find_all('div', {'class': 'product-item-holder'})
        for obj in data_obj:
            try:
                self.get_detail_of_single_product_with_soup(obj)
            except Exception as e:
                pass

    def get_detail_of_single_product_with_soup(self, data_obj):
        img_container = data_obj.find('div', {'class': 'image-container'})
        img_tag = img_container.find('img')
        if img_tag:
            img_tag = img_tag.attrs['src']
        else:
            img_tag = ''

        href_link_ = img_container.find('a')
        href_link_ = 'https://www.gsmnet.ro' + str(href_link_.attrs['href'])

        title_price_info = data_obj.find('div', {'class': 'product-bottom'})
        title_ = title_price_info.find('div', {'class': 'body'})
        title_ = title_.find('h2', {'class': 'title'})
        title_ = title_.text
        title_ = title_.replace('\n', '')
        title_ = title_.strip()

        price_ = title_price_info.find('div', {'class': 'prices'})
        prev_price = price_.find('div', {'class': 'price-prev'})
        current_price = price_.find('div', {'class': 'price-current'})

        original_price = current_price.text
        promotional_price = current_price.text
        if prev_price:
            original_price = prev_price.text
            promotional_price = current_price.text

        new_product_check = data_obj.find('div', {'class': 'ribbon-container'})
        new_product_check = new_product_check.find('div', {'class': 'ribbon blue'})

        if not new_product_check:
            self.is_not_new_product = True
            return

        dict_ = {
            'title': title_.strip(),
            'original_price': original_price.strip(),
            'promotional_price': promotional_price.strip(),
            'href_link': href_link_.strip(),
            'img_tag': img_tag
        }
        self.resultant_list.append(dict_)

    def get_pagination_information(self):
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        pagination_info = soup.find('ul', {'class': 'pagination'})
        list_elements = pagination_info.find_all('li')[-2]
        last_page = list_elements.find('a').attrs['href']
        last_page = last_page.split('/')[2]
        last_page = last_page.split(':')[1]
        self.pagination_info = int(last_page)
        self.driver.implicitly_wait(10)


# mgz = GsmnetInformationNewProducts()
# mgz.get_products_page()
# print(mgz.resultant_list)
