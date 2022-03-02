import os

from django.conf import settings

from .utils import *


def export_rule_to_file(rule_type):
    directory_path = os.path.join('products', 'templates', 'products', 'export_rules')
    file_path = os.path.join(settings.BASE_DIR, directory_path)

    if rule_type == 4:
        file_path = os.path.join(file_path, 'export_local_cost.csv')
        file_path = open(file_path, "w")

        file_path.write(
            "additional cost,cost unit,higher price,additional price,price unit,supplier,category,product\n")
        lcs_ = Rules.objects.filter(rule_type=4)
        for obj in lcs_:
            response_ = get_local_cost_supplier(obj)
            if response_:
                product_ = response_['product']
                if not product_:
                    product_ = ""
                response_ = str(response_['cost']) + "," + response_['cost_unit'] + "," \
                            + str(response_['price']) + "," + str(response_['percentage']) + "," \
                            + response_['percentage_unit'] + "," + response_['supplier'] + "," \
                            + response_['category'] + "," + product_ + "\n"
                file_path.write(response_)

        file_path.close()

    if rule_type == 5:
        file_path = os.path.join(file_path, 'export_thenx_cost.csv')
        file_path = open(file_path, "w")

        file_path.write(
            "additional cost,cost unit,higher price,additional price,price unit,supplier,category,product\n")

        tcs_ = Rules.objects.filter(rule_type=5)
        for obj in tcs_:
            response_ = get_thenx_cost_supplier(obj)
            if response_:
                product_ = response_['product']
                if not product_:
                    product_ = ""
                response_ = str(response_['cost']) + "," + response_['cost_unit'] + "," \
                            + str(response_['price']) + "," + str(response_['percentage']) + "," \
                            + response_['percentage_unit'] + "," + response_['supplier'] + "," \
                            + response_['category'] + "," + product_ + "\n"
                file_path.write(response_)

        file_path.close()

    if rule_type == 3:
        file_path = os.path.join(file_path, 'export_margin_rule.csv')
        file_path = open(file_path, "w")

        file_path.write(
            "margin type,margin price,price unit,supplier,category,product,higher price dependancy,"
            "lower price dependancy,lower price,lower price "
            "unit,higher price,higher price unit\n")

        margin_rules_ = Rules.objects.filter(rule_type=3)
        for obj in margin_rules_:
            response_ = get_margin_rule(obj)
            if response_:
                product_ = response_['product']
                if not product_:
                    product_ = ""
                response_ = str(response_['margin_type_export']) + "," + str(response_['percentage']) + "," \
                            + str(response_['percentage_unit']) + "," + str(response_['supplier']) + "," \
                            + response_['category'] + "," + product_ + "," + str(response_['price_dependancy']) \
                            + "," + str(response_['price_dependancy2']) \
                            + "," + str(response_['lower_percentage']) + "," \
                            + response_['lower_percentage_unit'] + "," + str(response_['higher_percentage']) + "," \
                            + response_['higher_percentage_unit'] + "\n"
                file_path.write(response_)

        file_path.close()


def export_product_to_file():
    directory_path = os.path.join('products', 'templates', 'products', 'export_pages')
    file_path = os.path.join(settings.BASE_DIR, directory_path)

    file_path = os.path.join(file_path, 'products.csv')
    file_path = open(file_path, "w")

    csv_writer = csv.writer(file_path, lineterminator='\n')

    # csv_writer.writerow(header)  # write header
    file_path.write(
        "sku,categories,name,supplier,supplier price,bank exchange rate,supplier price ron,local c.,thenx c,"
        "vat,all cost price,last all cost,margin whole, margin retail,whole price,retail price,last retail price & date,"
        "smart price,cheap comp\n")

    products = Products.objects.all()

    final_list = []
    for obj in products.iterator():
        sku = obj.sku
        categories = []
        for obj2 in obj.categories.all():
            categories.append(obj2.name)
        categories = ':'.join(categories)
        name = obj.name
        supplier = ""
        if obj.supplier:
            supplier = obj.supplier.name

        bank_exchange = ''
        if obj.currency_code == 1:
            bank_exchange = 'EUR'
        elif obj.currency_code == 2:
            bank_exchange = 'USD'
        elif obj.currency_code == 3:
            bank_exchange = 'CNY'
        elif obj.currency_code == 4:
            bank_exchange = 'RON'
        supp_price = str(bank_exchange) + " " + str(round(obj.supplier_price_ron, 2))
        bank_exchange = round(obj.exchange_rate, 2)
        supp_price_ron = round(obj.cost, 2)
        local_cost = round(obj.local_cost, 2)
        thenx_cost = round(obj.thenx_cost, 2)
        vat = 1.19

        all_cost_price = round(obj.all_cost_price, 2)

        margin_whole_sale_unit = obj.margin_whole_sale_unit
        if margin_whole_sale_unit == 1:
            margin_whole_sale_unit = '$'
        elif margin_whole_sale_unit == 1:
            margin_whole_sale_unit = '%'
        else:
            margin_whole_sale_unit = ''

        margin_retail_unit = obj.margin_retail_unit
        if margin_retail_unit == 1:
            margin_retail_unit = '$'
        elif margin_retail_unit == 1:
            margin_retail_unit = '%'
        else:
            margin_retail_unit = ''

        whole_sale_price = round(obj.whole_sale_price, 2)
        retail_price = round(obj.retail_price, 2)

        margin_whole_sale = str(round(obj.margin_whole_sale, 2)) + str(margin_whole_sale_unit)
        margin_retail = str(round(obj.margin_retail, 2)) + str(margin_retail_unit)

        old_retail_date = ''
        if obj.old_retail_date:
            old_retail_date = str(round(obj.old_retail_price, 2)) + ' - ' + str(obj.old_retail_date)

        smart_price = ''
        if obj.is_smart_price_already_set:
            smart_price = round(obj.smart_price_value, 2)

        cheapest_comp = ''
        if obj.cheapest_comp:
            cheapest_comp = obj.cheapest_comp

        response_ = [str(sku), str(categories), str(name), str(supplier), str(supp_price), str(bank_exchange),
                     str(supp_price_ron), str(local_cost), str(thenx_cost), str(vat), str(all_cost_price),
                     str(margin_whole_sale), str(margin_retail),
                     str(whole_sale_price), str(retail_price), str(old_retail_date), str(smart_price),
                     str(cheapest_comp)]
        final_list.append(response_)

    for obj in final_list:
        try:
            csv_writer.writerow(obj)
        except:
            print (obj[0])

    file_path.close()


def export_scraping_to_file():
    directory_path = os.path.join('products', 'templates', 'products', 'export_pages')
    file_path = os.path.join(settings.BASE_DIR, directory_path)

    file_path = os.path.join(file_path, 'products.csv')
    file_path = open(file_path, "w", encoding="utf-8")

    csv_writer = csv.writer(file_path)

    # csv_writer.writerow(header)  # write header
    file_path.write(
        "sku,categories,name,supplier,supplier price,bank exchange rate,supplier price ron,local c.,thenx c,"
        "vat,all cost price,last all cost,margin whole, margin retail,whole price,retail price,last retail price & date,"
        "smart price,cheap comp\n")

    products = Products.objects.all()

    final_list = []
    for obj in products.iterator():
        sku = obj.sku
        categories = []
        for obj2 in obj.categories.all():
            categories.append(obj2.name)
        categories = ':'.join(categories)
        name = obj.name
        supplier = ""
        if obj.supplier:
            supplier = obj.supplier.name

        bank_exchange = ''
        if obj.currency_code == 1:
            bank_exchange = 'EUR'
        elif obj.currency_code == 2:
            bank_exchange = 'USD'
        elif obj.currency_code == 3:
            bank_exchange = 'CNY'
        elif obj.currency_code == 4:
            bank_exchange = 'RON'
        supp_price = str(bank_exchange) + " " + str(round(obj.supplier_price_ron, 2))
        bank_exchange = round(obj.exchange_rate, 2)
        supp_price_ron = round(obj.cost, 2)
        local_cost = round(obj.local_cost, 2)
        thenx_cost = round(obj.thenx_cost, 2)
        vat = 1.19

        all_cost_price = round(obj.all_cost_price, 2)

        margin_whole_sale_unit = obj.margin_whole_sale_unit
        if margin_whole_sale_unit == 1:
            margin_whole_sale_unit = '$'
        elif margin_whole_sale_unit == 1:
            margin_whole_sale_unit = '%'
        else:
            margin_whole_sale_unit = ''

        margin_retail_unit = obj.margin_retail_unit
        if margin_retail_unit == 1:
            margin_retail_unit = '$'
        elif margin_retail_unit == 1:
            margin_retail_unit = '%'
        else:
            margin_retail_unit = ''

        whole_sale_price = round(obj.whole_sale_price, 2)
        retail_price = round(obj.retail_price, 2)

        margin_whole_sale = str(round(obj.margin_whole_sale, 2)) + str(margin_whole_sale_unit)
        margin_retail = str(round(obj.margin_retail, 2)) + str(margin_retail_unit)

        old_retail_date = ''
        if obj.old_retail_date:
            old_retail_date = str(round(obj.old_retail_price, 2)) + ' - ' + str(obj.old_retail_date)

        smart_price = ''
        if obj.is_smart_price_already_set:
            smart_price = round(obj.smart_price_value, 2)

        cheapest_comp = ''
        if obj.cheapest_comp:
            cheapest_comp = obj.cheapest_comp

        response_ = [str(sku), str(categories), str(name), str(supplier), str(supp_price), str(bank_exchange),
                     str(supp_price_ron), str(local_cost), str(thenx_cost), str(vat), str(all_cost_price),
                     str(margin_whole_sale), str(margin_retail),
                     str(whole_sale_price), str(retail_price), str(old_retail_date), str(smart_price),
                     str(cheapest_comp)]
        final_list.append(response_)

    csv_writer.writerows(final_list)

    file_path.close()
