BASE_URL = 'http://dev.thenx.net/rest/V1/'
AUTHORIZATION_TOKEN = '7h5om9dna1pljz1mkbwqr4pzxcih1m79'
COOKIE = 'PHPSESSID=e19493074191370937fe91928154d29c'
HEADERS = {'Authorization': 'Bearer ' + AUTHORIZATION_TOKEN, 'Cookie': COOKIE}
CATEGOIRES_LIST_URL = 'categories/list?searchCriteria'
CATEGOIRES_URL = 'categories?rootCategoryId=1'
BRANDS_URL = 'products/attributes/brand/options'
SUPPLIERS_URL = 'products/attributes/supplier/options'
PRODUCTS_URL = 'thenx/xrfeed/'
PAYLOAD = {}

LOCAL_COST_OF_SUPPLIER_IN_PERCENTAGE = 7.0
LOCAL_COST_OF_THENX_IN_PERCENTAGE = 2
DEFAULT_VAT_OF_SUPPLIER = 19

# New Services
CATEGORIES_SERVICES = "https://square-company.ro/_API/thenx/product_price_sync/category_list.php?key=TNXIEf7jzLLJXsepQGYZJ6wIPoFtrVIc"
SUPPLIER_SERVICES = "https://square-company.ro/_API/thenx/product_price_sync/suppliers.php?key=TNXIEf7jzLLJXsepQGYZJ6wIPoFtrVIc"
BRAND_SERVICES = "https://square-company.ro/_API/thenx/product_price_sync/brands.php?key=TNXIEf7jzLLJXsepQGYZJ6wIPoFtrVIc"
PRODUCT_SERVICES = "https://square-company.ro/_API/thenx/product_price_sync/products.php?key=TNXIEf7jzLLJXsepQGYZJ6wIPoFtrVIc"
COMPETITOR_FETCHING_LINK = "http://www.square-company.ro/_API/thenx/product_price_sync/export_competitors.php?key=TNXIEf7jzLLJXsepQGYZJ6wIPoFtrVIc"
PRICE_UPDATION_OVER_SERVER = "https://square-company.ro/_API/thenx/product_price_sync/import_price.php"

EMAIL_ = 'meharbanliaquat@gmail.com'

CURRENCY_CODES = {'EUR': 1, 'USD': 2, 'CNY': 3, 'RON': 4}