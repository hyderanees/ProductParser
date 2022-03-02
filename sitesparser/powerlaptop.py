import requests
from bs4 import BeautifulSoup


class PowerLaptopInformation:
    def __init__(self, href_link):
        self.url = href_link
        self.soup = self.get_page()

    def get_page(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup.find('div', {'class': 'ProductDetailsGrid'})

    def get_stock_value(self):
        stock_value = 'N/A'
        try:
            divs_ = self.soup.find_all('div', {'class': 'DetailRow'})
            for obj in divs_:

                all_divs = obj.find_all('div')
                label_check = all_divs[0].text.strip()

                if label_check == 'Stoc:':
                    stock_ = all_divs[1]
                    stock_ = stock_.text.strip()

                    if stock_.lower() == 'momentan indisponibil' or stock_.lower() == 'currently unavailable' \
                            or stock_.lower() == 'stoc epuizat' or stock_.lower() == 'lipsa stoc' or stock_.lower() == 'curand' \
                            or stock_.lower() == 'lack of stock' or stock_.lower() == 'out-of-stock' or stock_.lower() == '':
                        stock_value = 'no stock'
                    elif stock_.lower() == 'in stock' or stock_.lower() == 'in stoc':
                        stock_value = 'in stock'
                    elif stock_.lower() == 'precomanda':
                        stock_value = 'pre-order'
                    else:
                        stock_value = 'N/A'
                    break
        except:
            stock_value = 'N/A'
        return stock_value

    def get_prices(self):
        count_ = 0
        original_price = 0
        promotion_price = 0

        divs_ = self.soup.find_all('div', {'class': 'DetailRow'})

        for obj in divs_:
            value_ = obj.find('div', {'class': 'Value'})
            if count_ == 0:
                original_price = value_.text.replace('Lei', '').strip()
                original_price = original_price.replace('(VAT included)', '')
                original_price = original_price.replace('(TVA inclus)', '')
            elif count_ == 1:
                promotion_price = value_.text.replace('Lei', '').strip()
                promotion_price = promotion_price.replace('(TVA inclus)', '')
                promotion_price = promotion_price.replace('(VAT included)', '')
                promotion_price = promotion_price.split('\n')[0]
                promotion_price = promotion_price.strip()
            count_ = count_ + 1
            if count_ > 2:
                break

        original_price = float(original_price)
        promotion_price = float(promotion_price)

        stock = self.get_stock_value()
        print('Original Price#\t', original_price, '\tPromotion Price#\t', promotion_price, '\tStock\t', stock)
        return {'url': self.url, 'original_price': original_price, 'promotion_price': promotion_price, 'stock': stock}


# url = "https://www.powerlaptop.ro/products/hdd-caddy-laptop-9mm-intern-sata-extern-sata.html"
# PowerLaptopInformation(url).get_prices()
