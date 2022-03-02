import requests
import xmltodict

EXCHANGE_RATE = 'https://www.bnr.ro/nbrfxrates.xml'

prices = {
    1: 0.0,
    2: 0.0,
    3: 0.0
}


def get_prices():
    response = requests.get(EXCHANGE_RATE)
    data = xmltodict.parse(response.content)
    data = data['DataSet']['Body']['Cube']['Rate']
    for obj in data:
        currency = obj['@currency']
        rate = obj['#text']

        if currency == 'CNY':
            prices[3] = float(rate)

        if currency == 'EUR':
            prices[1] = float(rate)

        if currency == 'USD':
            prices[2] = float(rate)

    return prices
