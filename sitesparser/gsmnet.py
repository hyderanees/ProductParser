import requests
from bs4 import BeautifulSoup


class GSMNETInformation:
    def __init__(self, href_link):
        self.url = href_link
        self.soup = self.get_page()

    def get_page(self):
        page = requests.get(self.url)
        return BeautifulSoup(page.text, "html.parser")

    def get_stock_value(self):
        try:
            stock_ = self.soup.find('div', {'class': 'stock-wishlist-single'})
            stock_ = stock_.find_all('span')[1].text.strip()

            if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                    or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand'\
                    or stock_.lower() == 'lack of stock':
                stock_ = 'no stock'
            elif stock_.lower() == 'in stoc' or stock_.lower() == 'in stock':
                stock_ = 'in stock'
            else:
                stock_ = 'N/A'
        except:
            stock_ = 'N/A'
        return stock_

    def get_prices(self):
        price_obj = self.soup.find('div', {'class': 'prices'})
        original_price = price_obj.find('div', {'class': 'price-current'})
        original_price = original_price.contents[0]
        original_price = original_price.replace('.', '').strip()
        # original_price = original_price.text.replace('LEI', '').strip()

        discount_check = price_obj.find('div', {'class': 'price-prev'})
        if discount_check:
            value_ = discount_check.contents[0]
            value_ = value_.replace('.', '').strip()
            promotion_price = value_
        else:
            promotion_price = original_price

        original_price = float(original_price)
        promotion_price = float(promotion_price)

        stock = self.get_stock_value()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


# url = "https://www.gsmnet.ro/accesorii-telefoane-tablete-incarcatoare/incarcator-auto-dual-usb-usb-type-c-samsung-ep-ln920cbegww-fast-charging"
# GSMNETInformation(url).get_prices()
