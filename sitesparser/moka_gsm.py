import requests
from bs4 import BeautifulSoup


class MokaGSMInformation:
    def __init__(self, href_link):
        self.url = href_link
        self.soup = self.get_page()

    def get_page(self):
        page = requests.get(self.url)
        return BeautifulSoup(page.text, "html.parser")

    def get_stock_value(self):
        try:
            stock_ = self.soup.find('span', {'class': 'stock-status'})
            stock_ = stock_.text.strip()

            if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                    or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand' \
                    or stock_.lower() == 'lack of stock' or stock_.lower() == 'out-of-stock':
                stock_ = 'no stock'
            elif stock_ == 'În Stoc' or stock_.lower() == 'in stock' or stock_.lower() == 'in stoc':
                stock_ = 'in stock'
            else:
                stock_ = 'N/A'
        except:
            stock_ = 'N/A'
        return stock_

    def get_prices(self):
        original_price = self.soup.find_all('input', {'id': 'productBasePrice'})
        promotion_price = self.soup.find_all('input', {'id': 'productFinalPrice'})
        original_price = original_price[0].attrs['value']
        promotion_price = promotion_price[0].attrs['value']

        original_price = float(original_price)
        promotion_price = float(promotion_price)

        stock = self.get_stock_value()

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


# url = "https://www.moka-gsm.ro/display-uri-si-touchscreen-uri/ecran-display-huawei-psmart-2019-p-smart-2019-original.html"
# url2 = "https://www.moka-gsm.ro/piese-electrocasnice/curea-curea-ms-1204h8-481235818167.html"
# MokaGSMInformation(url2).get_prices()
