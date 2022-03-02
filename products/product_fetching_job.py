from products.models import *
from products.utils import get_products_list, calculate_price_detail_of_product
from .read_xml_exchange_rate import get_prices
import datetime


def product_fetching_jobs():
    cron_ = CronJobLogRunning.objects.create(cron_job_type=0)
    data = get_products_list()

    products_list_info = []
    data, brands_id, supplier_ids_list, categories_id = data
    data2 = data[:]

    prices_rate = get_prices()

    scanned_items = len(data)
    changed_prices = 0

    brand_ids = [int(x['id']) for x in brands_id]
    existing_brands = Brands.objects.filter(id__in=brand_ids).values_list('id', flat=True)
    brands_to_create = list(set(brand_ids) - set(existing_brands))
    brands_to_create = list(filter(lambda x: int(x['id']) in brands_to_create, brands_id))
    brands_to_create = list({x['id']: x for x in brands_to_create}.values())
    Brands.objects.bulk_create([Brands(id=x['id'], reference_id=x['id'], name=x['name']) for x in brands_to_create])

    category_ids = [int(x['id']) for x in categories_id]
    existing_category = Categories.objects.filter(id__in=category_ids).values_list('id', flat=True)
    category_to_create = list(set(category_ids) - set(existing_category))
    category_to_create = list(filter(lambda x: int(x['id']) in category_to_create, categories_id))
    category_to_create = list({x['id']: x for x in category_to_create}.values())
    Categories.objects.bulk_create(
        [Categories(id=x['id'], reference_id=x['id'], name=x['name']) for x in category_to_create])

    supplier_ids = [int(x['id']) for x in supplier_ids_list]
    existing_suppliers = Suppliers.objects.filter(id__in=supplier_ids).values_list('id', flat=True)
    supplier_to_create = list(set(supplier_ids) - set(existing_suppliers))
    supplier_to_create = list(filter(lambda x: int(x['id']) in supplier_to_create, supplier_ids_list))
    supplier_to_create = list({x['id']: x for x in supplier_to_create}.values())
    Suppliers.objects.bulk_create(
        [Suppliers(id=x['id'], reference_id=x['id'], name=x['name']) for x in supplier_to_create])

    product_ids = [int(x['id']) for x in data]
    existing_products = Products.objects.filter(id__in=product_ids).values_list('id', flat=True)
    products_to_create = list(set(product_ids) - set(existing_products))
    products_to_create = list(filter(lambda x: int(x['id']) in products_to_create, data))
    products_to_create = list({x['id']: x for x in products_to_create}.values())

    new_sku = len(products_to_create)
    product_category_list = []
    new_products_check_list = []
    for obj in products_to_create:
        if obj['brand_id'] and obj['supplier_id']:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'],
                         currency_code=obj['currency_code'],
                         quantity=obj['quantity'],
                         cost=float(obj['cost']),
                         price=float(obj['price']), brand_id=int(obj['brand_id']),
                         supplier_id=int(obj['supplier_id'])))
        elif obj['brand_id']:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'], cost=float(obj['cost']),
                         quantity=obj['quantity'],
                         currency_code=obj['currency_code'],
                         price=float(obj['price']), brand_id=int(obj['brand_id'])))
        elif obj['supplier_id']:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'], cost=float(obj['cost']),
                         quantity=obj['quantity'],
                         currency_code=obj['currency_code'],
                         price=float(obj['price']), supplier_id=int(obj['supplier_id'])))
        else:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'], cost=float(obj['cost']),
                         quantity=obj['quantity'],
                         currency_code=obj['currency_code'],
                         price=float(obj['price'])))

        [product_category_list.append(
            Products.categories.through(categories_id=int(cat['category_id']), products_id=int(obj['id']))) for cat in
            obj['categories']]

    Products.objects.bulk_create(products_list_info)
    Products.categories.through.objects.bulk_create(product_category_list)

    for obj in data2:
        try:
            pro, created = Products.objects.update_or_create(id=obj['id'],
                                                             defaults=dict(url=obj['url'], cost=float(obj['cost']),
                                                                           quantity=obj['quantity'], sku=obj['sku'],
                                                                           name=obj['name'],

                                                                           currency_code=obj['currency_code'],
                                                                           price=float(obj['price'])))
            new_products_check_list.append(pro.id)
            if created:
                changed_prices = changed_prices + 1

            cost_check = pro.supplier_price_ron

            sup_ = Suppliers.objects.get(id=int(obj['supplier_id']))
            brand_ = Brands.objects.get(id=int(obj['brand_id']))

            pro.supplier = sup_
            pro.brand = brand_
            pro.supplier_price_ron = pro.cost
            pro.save()

            pro.categories.remove(*pro.categories.all())

            for cat in obj['categories']:
                categories_ = Categories.objects.get(id=int(cat['category_id']))
                pro.categories.add(categories_)
                pro.save()

            if cost_check != pro.supplier_price_ron:
                if pro.currency_code in [1, 2, 3]:
                    pro.cost = pro.cost * prices_rate[pro.currency_code]
                    pro.exchange_rate = prices_rate[pro.currency_code]
                    pro.save()
            elif pro.supplier_price_ron == cost_check:
                if pro.currency_code in [1, 2, 3]:
                    pro.cost = pro.cost * prices_rate[pro.currency_code]
                    pro.exchange_rate = prices_rate[pro.currency_code]
                    pro.save()

            response_ = calculate_price_detail_of_product(pro)

            local_cost_supplier = response_['local_cost']
            local_cost_supplier_check = response_['local_cost_is']
            if local_cost_supplier_check != 'N/A':
                local_cost_supplier = round(local_cost_supplier, 2)
            else:
                local_cost_supplier = 0

            thenx_cost_supplier = response_['thenx_cost']
            thenx_cost_supplier_check = response_['thenx_cost_is']
            if thenx_cost_supplier_check != 'N/A':
                thenx_cost_supplier = round(thenx_cost_supplier, 2)
            else:
                thenx_cost_supplier = 0

            all_cost_price = response_['all_cost_price']
            if all_cost_price and all_cost_price != 'N/A':
                all_cost_price = round(all_cost_price, 2)
            else:
                all_cost_price = 0

            whole_sale_price = response_['whole_sale_rounded']
            if whole_sale_price and whole_sale_price != 'N/A':
                whole_sale_price = round(whole_sale_price, 2)
            else:
                whole_sale_price = 0

            whole_sale_margin = response_['whole_sale_margin']
            if whole_sale_margin and whole_sale_margin != 'N/A':
                whole_sale_margin = round(whole_sale_margin, 2)
            else:
                whole_sale_margin = 0

            margin_whole_sale_unit = response_['whole_sale_rule_unit']
            if margin_whole_sale_unit and margin_whole_sale_unit != 'N/A':
                try:
                    if margin_whole_sale_unit == 'Percent':
                        margin_whole_sale_unit = 2
                    else:
                        margin_whole_sale_unit = 1
                except Exception as e:
                    margin_whole_sale_unit = 0
            else:
                margin_whole_sale_unit = 0

            retail_sale_price = response_['retail_price_rounded']
            if retail_sale_price and retail_sale_price != 'N/A':
                retail_sale_price = round(retail_sale_price, 2)
            else:
                retail_sale_price = 0

            retail_price_margin = response_['retail_price_margin']
            if retail_price_margin and retail_price_margin != 'N/A':
                retail_price_margin = round(retail_price_margin, 2)
            else:
                retail_price_margin = 0

            margin_retail_unit = response_['retail_price_rule_unit']
            if margin_retail_unit and margin_retail_unit != 'N/A':
                try:
                    if margin_retail_unit == 'Percent':
                        margin_retail_unit = 2
                    else:
                        margin_retail_unit = 1
                except Exception as e:
                    margin_retail_unit = 0
            else:
                margin_retail_unit = 0

            if retail_sale_price and retail_sale_price != pro.old_retail_price:
                pro.old_retail_price = pro.retail_price
                pro.old_retail_date = datetime.datetime.now().date()

            if all_cost_price and all_cost_price != pro.old_all_cost_price:
                pro.old_all_cost_price = pro.all_cost_price
                pro.old_all_cost_date = datetime.datetime.now().date()

            pro.retail_price = retail_sale_price
            pro.margin_retail = retail_price_margin
            pro.margin_retail_unit = margin_retail_unit
            pro.margin_whole_sale_unit = margin_whole_sale_unit
            pro.margin_whole_sale = whole_sale_margin
            pro.whole_sale_price = whole_sale_price
            pro.all_cost_price = all_cost_price
            pro.local_cost = local_cost_supplier
            pro.thenx_cost = thenx_cost_supplier

            pro.save()

        except Exception as e:
            pass

    Products.objects.all().exclude(id__in=new_products_check_list).delete()

    cron_.scanned_sku = scanned_items
    cron_.new_sku = new_sku
    cron_.changed_prices = changed_prices
    cron_.save()
