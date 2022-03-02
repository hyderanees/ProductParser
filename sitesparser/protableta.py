import requests
from bs4 import BeautifulSoup


class ProtabletaInformation:
    def __init__(self, href_link):
        self.url = href_link
        self.soup = self.get_page()

    def get_page(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find('div', {'class': 'ro-product-price-meta'})

    def get_prices(self):
        price_obj = self.soup.find('span', {'class': 'woocommerce-Price-amount'})
        original_price = price_obj.text.replace('lei', '').strip()
        promotion_price = original_price

        original_price = original_price.replace(',', '.')
        promotion_price = promotion_price.replace(',', '.')

        original_price = float(original_price)
        promotion_price = float(promotion_price)

        stock = self.get_stock()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}

    def get_stock(self):
        try:
            stock_ = self.soup.find('div', {'class': 'stock'})
            stock_ = stock_.text.replace('Disponibilitate:', '').strip()

            if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                    or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand' \
                    or stock_.lower() == 'lack of stock' or stock_.lower() == 'out-of-stock' or stock_.lower() == '':
                stock_ = 'no stock'
            elif stock_ == 'În Stoc' or stock_.lower() == 'in stock' or stock_.lower() == 'in stoc':
                stock_ = 'in stock'
            else:
                stock_ = 'N/A'
        except:
            stock_ = 'N/A'
        return stock_


# url = "https://www.protableta.ro/shop/piese-telefoane/ansamblu-telefon-mobil/display-ecran-lcd-afisaj-huawei-jny-l21a/"
# pti = ProtabletaInformation(url).get_prices()
