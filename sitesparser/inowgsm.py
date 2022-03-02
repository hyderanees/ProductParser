import requests
from bs4 import BeautifulSoup


class InowGSMInformation:
    def __init__(self, href_link):
        self.url = href_link
        self.soup = self.get_page()

    def get_page(self):
        page = requests.get(self.url)
        return BeautifulSoup(page.text, "html.parser")

    def get_stock_value(self):
        try:
            stock_ = self.soup.find('li', {'class': 'product-stock'})
            stock_ = stock_.find('span').text.strip()
            if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                    or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand'\
                    or stock_.lower() == 'lack of stock':
                stock_ = 'no stock'
            elif stock_ == 'În Stoc' or stock_.lower() == 'in stock' or stock_.lower() == 'in stoc':
                stock_ = 'in stock'
            else:
                stock_ = 'N/A'
        except:
            stock_ = 'N/A'
        return stock_

    def get_prices(self):
        price_obj = self.soup.find('div', {'class': 'product-price-group'})
        price_obj = price_obj.find('div', {'class': 'price-group'})

        original_price = price_obj.find('div', {'class': 'product-price'})
        if original_price:
            original_price = original_price.text.replace('Lei', '')
            promotion_price = original_price
        else:
            promotion_price = price_obj.find('div', {'class': 'product-price-new'})
            original_price = price_obj.find('div', {'class': 'product-price-old'})
            promotion_price = promotion_price.text.replace('Lei', '')
            original_price = original_price.text.replace('Lei', '')

        original_price = original_price.replace(',', '.')
        promotion_price = promotion_price.replace(',', '.')

        original_price = float(original_price)
        promotion_price = float(promotion_price)
        stock = self.get_stock_value()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


# url = "https://www.inowgsm.ro/touchscreen-telefon/touchscreen-digitizer-geam-sticla-lenovo-k6-note-k53a48"
# InowGSMInformation(url).get_prices()
