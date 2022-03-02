import requests
from bs4 import BeautifulSoup


class ServicePackInformation:
    def __init__(self, href_link):
        self.url = href_link
        self.soup = self.get_page()

    def get_page(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find('div', {'class': 'summary entry-summary'})

    def get_stock_value(self):
        try:
            stock_ = self.soup.find('div', {'class': 'stock-wishlist-single'})
            stock_ = stock_.find_all('span')[1].text.strip()

            if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                    or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand' \
                    or stock_.lower() == 'lack of stock' or stock_.lower() == 'out-of-stock' or stock_.lower() == '':
                stock_ = 'no stock'
            elif stock_.lower() == 'in stoc' or stock_.lower() == 'in stock':
                stock_ = 'in stock'
            else:
                stock_ = 'N/A'
        except:
            stock_ = 'N/A'
        return stock_

    def get_prices(self):
        price_obj = self.soup.find_all('span', {'class': 'woocommerce-Price-amount amount'})
        if len(price_obj) > 1:
            promotion_price = price_obj[0].text.replace('lei', '')
            original_price = price_obj[1].text.replace('lei', '')
        else:
            original_price = price_obj[0].text.replace('lei', '')
            promotion_price = original_price

        try:
            original_price_ = original_price.split(',')[0]
            original_price_ = original_price_.replace('.', '')
        except:
            original_price_ = original_price
        try:
            promotion_price_ = promotion_price.split(',')[0]
            promotion_price_ = promotion_price_.replace('.', '')
        except:
            promotion_price_ = promotion_price

        original_price = original_price_.replace(',', '.')
        promotion_price = promotion_price_.replace(',', '.')

        original_price = float(original_price)
        promotion_price = float(promotion_price)

        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', 'N/A')
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': 'N/A'}


# url = "https://servicepack.ro/produs/display-p40-pro/?attribute_pa_culoare=blush-gold"
# ServicePackInformation(url).get_prices()
#