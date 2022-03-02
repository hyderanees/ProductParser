import csv
import datetime
import json

import requests
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import *


def get_categories_list():
    url = BASE_URL + CATEGOIRES_LIST_URL
    response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
    response = json.loads(response.content.decode("utf-8"))
    items = response['items']
    items_list = []
    for obj in items:
        items_list.append({'id': obj['id'], 'name': obj['name']})
    return items_list


def decode_children_data(list_):
    items_list = []
    for obj in list_:
        if len(obj['children_data']) > 0:
            response__ = decode_children_data(obj['children_data'])
            items_list = items_list + response__
        items_list.append({'id': int(obj['id']), 'reference_id': obj['id'], 'name': obj['name'],
                           'products_count': obj['product_count']})
    return items_list


def get_categories_list_with_product_count():
    url = BASE_URL + CATEGOIRES_URL
    response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
    response = json.loads(response.content.decode("utf-8"))
    items_list = [{'id': int(response['id']), 'reference_id': response['id'], 'name': response['name'],
                   'products_count': response['product_count']}]
    response__ = decode_children_data(response['children_data'])
    items_list = items_list + response__
    return items_list


def get_categories_list_new():
    url = CATEGORIES_SERVICES
    response = requests.request("GET", url)
    response = json.loads(response.content.decode("utf-8"))
    response = [{'id': int(obj['id']), 'reference_id': obj['id'], 'name': obj['name'],
                 'products_count': 0} for obj in response]
    return response


# def get_brands_information():
#     url = BASE_URL + BRANDS_URL
#     response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
#     response = json.loads(response.content.decode("utf-8"))
#     items_list = []
#     for obj in response:
#         if obj['value']:
#             items_list.append({'id': int(obj['value']), 'reference_id': obj['value'], 'name': obj['label']})
#     return items_list


# def get_suppliers_information():
#     url = BASE_URL + SUPPLIERS_URL
#     response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
#     response = json.loads(response.content.decode("utf-8"))
#     items_list = []
#     for obj in response:
#         if obj['value']:
#             items_list.append({'id': int(obj['value']), 'reference_id': obj['value'], 'name': obj['label']})
#     return items_list


def get_suppliers_information():
    url = SUPPLIER_SERVICES
    response = requests.request("GET", url)
    response = json.loads(response.content.decode("utf-8"))
    response = [{'id': obj['id'], 'reference_id': obj['id'], 'name': obj['name']} for obj in response]
    return response


def get_brands_information():
    url = SUPPLIER_SERVICES
    response = requests.request("GET", url)
    response = json.loads(response.content.decode("utf-8"))
    response = [{'id': obj['id'], 'reference_id': obj['id'], 'name': obj['name']} for obj in response]
    return response


#
# def get_products_list():
#     url = BASE_URL + PRODUCTS_URL
#     response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
#     response = json.loads(response.content.decode("utf-8"))
#     response = json.loads(response)
#     items_list = []
#     brands_list = []
#     suppliers_list = []
#     categories_list_final_ = []
#     for obj in response:
#         categories = json.loads(obj['cat'])
#         categories_list = [{'category_id': x.split('__')[1], 'name': x.split('__')[0]} for x in categories]
#         if obj['price']:
#             price_ = obj['price']
#         else:
#             price_ = 0
#         if obj['cost']:
#             cost_ = obj['cost']
#         else:
#             cost_ = 0
#         items_list.append({'id': int(obj['id']), 'reference_id': obj['id'], 'name': obj['name'], 'sku': obj['sku'],
#                            'price': price_, 'url': obj['url'],
#                            'brand': obj['brand'], 'brand_id': obj['brand_id'],
#                            'supplier': obj['supplier'], 'supplier_id': obj['supplier_id'],
#                            'categories': categories_list,
#                            'cost': cost_
#                            })
#         if obj['brand_id']:
#             brands_list.append({'id': obj['brand_id'], 'name': obj['brand']})
#         if obj['supplier_id']:
#             suppliers_list.append({'id': obj['supplier_id'], 'name': obj['supplier']})
#         categories_list_ = [{'id': x.split('__')[1], 'name': x.split('__')[0]} for x in categories]
#         categories_list_final_ = categories_list_final_ + categories_list_
#     return items_list, brands_list, suppliers_list, categories_list_final_
#


def get_products_list():
    url = PRODUCT_SERVICES
    response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
    response = json.loads(response.content.decode("utf-8"))
    items_list = []
    brands_list = []
    suppliers_list = []
    categories_list_final_ = []
    for x, obj in response.items():
        categories_list = [{'category_id': obj['category_id'], 'name': obj['category']}]
        if obj['price']:
            price_ = obj['price']
        else:
            price_ = 0
        if obj['cost']:
            cost_ = obj['cost']
        else:
            cost_ = 0
        quantity = int(obj['quantity'])
        cost_currency = CURRENCY_CODES[obj['cost_currency']]
        items_list.append({'id': int(obj['id']), 'reference_id': obj['id'], 'name': obj['name'], 'sku': obj['sku'],
                           'price': price_, 'url': obj['product_url'],
                           'brand': obj['brand'], 'brand_id': obj['brand_id'],
                           'supplier': obj['supplier'], 'supplier_id': obj['supplier_id'],
                           'categories': categories_list,
                           'quantity': quantity,
                           'cost': cost_,
                           'currency_code': cost_currency
                           })
        if obj['brand_id']:
            brands_list.append({'id': obj['brand_id'], 'name': obj['brand']})
        if obj['supplier_id']:
            suppliers_list.append({'id': obj['supplier_id'], 'name': obj['supplier']})
        categories_list_ = [{'id': obj['category_id'], 'name': obj['category']}]
        categories_list_final_ = categories_list_final_ + categories_list_
    return items_list, brands_list, suppliers_list, categories_list_final_


def paginate(query, extract, start_index, length, draw):
    try:
        total = query.count()
    except:
        total = len(query)

    upper_limit = min(total, start_index + length)
    iteration = 0

    items = []
    key_finder = start_index + 1
    for item in query[start_index:upper_limit]:
        iteration = iteration + 1
        ext = extract(item, key_finder)
        if ext is not None:
            if type(ext) == list:
                for obj2 in ext:
                    items.append(obj2)
            else:
                items.append(ext)
            key_finder += 1

    return {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': items
    }


def get_dictionary_object(rule):
    if rule.rule_type == 1:
        return get_warranty_obj(rule)
    elif rule.rule_type == 2:
        return {'percentage': VatRule.objects.get(rule=rule).percentage,
                'rule_type': 'VAT Rule'}
    elif rule.rule_type == 3:
        return get_margin_rule(rule)
    elif rule.rule_type == 4:
        return get_local_cost_supplier(rule)
    elif rule.rule_type == 5:
        return get_thenx_cost_supplier(rule)


def get_warranty_obj(rule):
    try:
        wr = WarrantyRule.objects.get(rule=rule)
    except:
        rule.delete()
        return False

    if wr.is_all_suppliers:
        suppliers_ = 'All'
    else:
        suppliers_ = [x.name for x in wr.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    if wr.is_all_categories:
        categories_ = 'All'
    else:
        categories_ = [x.name for x in wr.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if wr.is_on_category:
        category_ = True
    if wr.product_sku:
        product_ = wr.product_sku.sku
    return {
        'days': wr.days,
        'supplier': suppliers_,
        'category': categories_,
        'is_category': category_,
        'product': product_,
        'rule_type': 'Warranty Rule',
        'rule_id': rule.id
    }


def get_margin_rule(rule):
    try:
        mr = MarginRules.objects.get(rule=rule)
    except:
        rule.delete()
        return False

    if mr.is_all_suppliers:
        suppliers_ = 'All'
    else:
        suppliers_ = [x.name for x in mr.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    margin_type = 'Retail Price'
    name_ = 'Margin (Retail Price)'
    margin_type_export = 'retail'
    if mr.type == 0:
        margin_type = 'Whole Sale'
        name_ = 'Margin (Whole Sale)'
        margin_type_export = 'wholesale'
    percentage = mr.percentage
    if mr.is_all_categories:
        categories_ = 'All'
    else:
        categories_ = [x.name for x in mr.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if mr.is_on_category:
        category_ = True
    if mr.product_sku:
        product_ = mr.product_sku.sku
    higher_price_val_1 = ''
    if mr.price_dependancy:
        higher_price_val_1 = str(mr.higher_percentage)
        if mr.higher_percentage_unit == 1:
            higher_price_val_1 += '$'
        else:
            higher_price_val_1 += '%'

    lower_price_val_1 = ''
    if mr.price_dependancy2:
        lower_price_val_1 = str(mr.lower_percentage)
        if mr.lower_percentage_unit == 1:
            lower_price_val_1 += '$'
        else:
            lower_price_val_1 += '%'
    return {
        'margin_type': margin_type,
        'higher_price_val': higher_price_val_1,
        'lower_price_val': lower_price_val_1,
        'margin_type_export': margin_type_export,
        'category': categories_,
        'is_category': category_,
        'product': product_,
        'percentage': percentage,
        'price_dependancy': mr.price_dependancy,
        'price_dependancy2': mr.price_dependancy2,
        'higher_percentage': mr.higher_percentage,
        'lower_percentage': mr.lower_percentage,
        'supplier': suppliers_,
        'rule_type': name_,
        'percentage_unit': get_unit_type(mr.percentage_unit),
        'percentage_unit_int': mr.percentage_unit,
        'higher_percentage_unit': get_unit_type(mr.higher_percentage_unit),
        'higher_percentage_unit_int': mr.higher_percentage_unit,
        'lower_percentage_unit': get_unit_type(mr.lower_percentage_unit),
        'lower_percentage_unit_int': mr.lower_percentage_unit,
        'margin_type_int': mr.type,
        'rule_id': rule.id,
        'created_at': datetime.datetime.strftime(rule.created_at, '%d/%m/%Y')
    }


def get_price_priority(obj):
    if obj == 1:
        return "higher"
    else:
        return "lower"


def get_competitor_priority(obj):
    if obj == 1:
        return "highest"
    elif obj == 2:
        return "average"
    else:
        return "lowest"


def get_price_unit(obj):
    if obj == 1:
        return "RON"
    else:
        return "Percentage"


def get_competitor_rule(rule):
    competitor = ''
    competitor_int = 0

    try:
        pcr = PriceCompetitorRule.objects.get(rule=rule)
    except:
        rule.delete()
        return False

    if pcr.is_all_competitors:
        competitor = 'All Competitors'
        competitor_int = 0
    else:
        if pcr.competitor:
            competitor = pcr.competitor.name
            competitor_int = pcr.competitor.id

    check_price = pcr.check_pricer
    check_price_unit = get_price_unit(pcr.check_pricer_unit)
    check_price_priority = get_price_priority(pcr.check_pricer_priority)
    competitor_priority = get_competitor_priority(pcr.competitor_priority)
    final_price_check = pcr.final_price_check
    final_price_unit = get_price_unit(pcr.final_price_unit)

    if pcr.is_all_suppliers:
        suppliers_ = 'All'
    else:
        suppliers_ = [x.name for x in pcr.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    if pcr.is_all_categories:
        categories_ = 'All'
    else:
        categories_ = [x.name for x in pcr.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if pcr.is_on_category:
        category_ = True
    if pcr.product_sku:
        product_ = pcr.product_sku.sku

    return {
        'competitor': competitor,
        'competitor_int': competitor_int,
        'check_price': check_price,
        'check_price_unit': check_price_unit,
        'check_price_unit_int': pcr.check_pricer_unit,
        'check_price_priority': check_price_priority,
        'check_price_priority_int': pcr.check_pricer_priority,
        'competitor_priority_int': pcr.competitor_priority,
        'competitor_priority': competitor_priority,
        'final_price_check': final_price_check,
        'final_price_unit': final_price_unit,
        'final_price_unit_int': pcr.final_price_unit,
        'rule_id': rule.id,
        'supplier': suppliers_,
        'category': categories_,
        'is_category': category_,
        'product': product_
    }


def get_unit_type(value):
    if value == 1:
        return "RON"
    else:
        return "Percent"


def get_local_cost_supplier(rule):
    try:
        lcp = LocalCostSupplier.objects.get(rule=rule)
    except:
        rule.delete()
        return False

    if lcp.is_all_suppliers:
        suppliers_ = 'All'
        suppliers_id_ = 0
    else:
        suppliers_id_ = [x.id for x in lcp.supplier.all()]
        suppliers_ = [x.name for x in lcp.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    if lcp.is_all_categories:
        categories_ = 'All'
        category_id_ = 0
    else:
        category_id_ = [x.id for x in lcp.category.all()]
        categories_ = [x.name for x in lcp.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if lcp.is_on_category:
        category_ = True
    if lcp.product_sku:
        product_ = lcp.product_sku.sku
    return {
        'supplier': suppliers_,
        'suppliers_id_': suppliers_id_,
        'category_id_': category_id_,
        'category': categories_,
        'is_category': category_,
        'product': product_,
        'cost': lcp.cost,
        'percentage': lcp.percentage,
        'price': lcp.price_dependancey,
        'rule_type': 'Local Cost Supplier',
        'rule_id': rule.id,
        'cost_unit': get_unit_type(lcp.cost_unit),
        'cost_unit_int': lcp.cost_unit,
        'percentage_unit_int': lcp.percentage_unit,
        'percentage_unit': get_unit_type(lcp.percentage_unit)
    }


def get_thenx_cost_supplier(rule):
    try:
        tcp = ThenxCostSupplier.objects.get(rule=rule)
    except:
        rule.delete()
        return False
    if tcp.is_all_suppliers:
        suppliers_ = 'All'
    else:
        suppliers_ = [x.name for x in tcp.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    if tcp.is_all_categories:
        categories_ = 'All'
    else:
        categories_ = [x.name for x in tcp.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if tcp.is_on_category:
        category_ = True
    if tcp.product_sku:
        product_ = tcp.product_sku.sku
    return {
        'supplier': suppliers_,
        'category': categories_,
        'is_category': category_,
        'product': product_,
        'cost': tcp.cost,
        'percentage': tcp.percentage,
        'price': tcp.price_dependancey,
        'rule_type': 'Thenx Cost Supplier',
        'rule_id': rule.id,
        'cost_unit': get_unit_type(tcp.cost_unit),
        'cost_unit_int': tcp.cost_unit,
        'percentage_unit': get_unit_type(tcp.percentage_unit),
        'percentage_unit_int': tcp.percentage_unit
    }


def get_lcs_obj(product):
    lcs_, is_lcs_cost_, local_cost_param_value, lcs_object = 0, 'N/A', 0, False

    if Rules.objects.filter(rule_type=4):
        categories__ = product.categories.all()

        filtered_ = LocalCostSupplier.objects.filter(is_on_category=False, product_sku=product).last()
        if not filtered_:
            filtered_ = LocalCostSupplier.objects.filter(is_on_category=True, supplier=product.supplier,
                                                         is_all_categories=False,
                                                         category__in=categories__)

            if not filtered_:
                filtered_ = LocalCostSupplier.objects.filter(is_on_category=True, supplier=product.supplier,
                                                             is_all_categories=True)

            if not filtered_:
                filtered_ = LocalCostSupplier.objects.filter(is_on_category=True, is_all_suppliers=True,
                                                             is_all_categories=True)

            if filtered_:
                filtered_ = filtered_.last()

        if filtered_:
            lcs_object = filtered_
            if product.cost > filtered_.price_dependancey:
                if filtered_.cost_unit == 1:
                    lcs_ = filtered_.cost
                    is_lcs_cost_ = True
                    local_cost_param_value = filtered_.cost
                else:
                    local_cost_param_value = filtered_.cost
                    lcs_ = (filtered_.cost / 100) * product.cost
                    is_lcs_cost_ = False
            else:
                if filtered_.percentage_unit == 1:
                    lcs_ = filtered_.percentage
                    is_lcs_cost_ = True
                    local_cost_param_value = filtered_.percentage
                else:
                    local_cost_param_value = filtered_.percentage
                    lcs_ = (filtered_.percentage / 100) * product.cost
                    is_lcs_cost_ = False
    return lcs_, is_lcs_cost_, local_cost_param_value, lcs_object


def get_tcs_obj(product):
    tcs_, is_tcs_cost_, thenx_cost_param_value, tcs_object = 0, 'N/A', 0, False

    if Rules.objects.filter(rule_type=5):
        categories__ = product.categories.all()

        filtered_ = ThenxCostSupplier.objects.filter(is_on_category=False, product_sku=product).last()
        if not filtered_:
            filtered_ = ThenxCostSupplier.objects.filter(is_on_category=True, supplier=product.supplier,
                                                         is_all_categories=False,
                                                         category__in=categories__)

            if not filtered_:
                filtered_ = ThenxCostSupplier.objects.filter(is_on_category=True, supplier=product.supplier,
                                                             is_all_categories=True)

            if not filtered_:
                filtered_ = ThenxCostSupplier.objects.filter(is_on_category=True, is_all_suppliers=True,
                                                             is_all_categories=True)

            if filtered_:
                filtered_ = filtered_.last()

        if filtered_:
            tcs_object = filtered_
            if product.cost > filtered_.price_dependancey:
                if filtered_.cost_unit == 1:
                    tcs_ = filtered_.cost
                    is_tcs_cost_ = True
                    thenx_cost_param_value = filtered_.cost
                else:
                    thenx_cost_param_value = filtered_.cost
                    tcs_ = (filtered_.cost / 100) * product.cost
                    is_tcs_cost_ = False
            else:
                if filtered_.percentage_unit == 1:
                    tcs_ = filtered_.percentage
                    is_tcs_cost_ = True
                    thenx_cost_param_value = filtered_.cost
                else:
                    thenx_cost_param_value = filtered_.percentage
                    tcs_ = (filtered_.percentage / 100) * product.cost
                    is_tcs_cost_ = False
    return tcs_, is_tcs_cost_, thenx_cost_param_value, tcs_object


def get_margin_rule_calculation(product, all_cost_price):
    mr = 'N/A'
    whole_sale = 'N/A'
    whole_sale_rounded = 'N/A'
    whole_sale_rule_unit = 'N/A'
    whole_sale_rule_identity = 'N/A'

    if MarginRules.objects.filter(rule__rule_type=3, type=0).exists():

        categories__ = product.categories.all()

        filtered_ = MarginRules.objects.filter(type=0, product_sku=product, is_on_category=False).last()
        if not filtered_:
            filtered_ = MarginRules.objects.filter(type=0, supplier=product.supplier, is_all_categories=False,
                                                   category__in=categories__, is_on_category=True)

            if not filtered_:
                filtered_ = MarginRules.objects.filter(type=0, supplier=product.supplier, is_all_categories=True,
                                                       is_on_category=True)

            if not filtered_:
                filtered_ = MarginRules.objects.filter(type=0, is_all_suppliers=True, is_all_categories=True,
                                                       is_on_category=True)

            if filtered_:
                filtered_ = filtered_.last()

        if filtered_:
            is_rule_applied_check_else_case = False
            whole_sale_rule_identity = filtered_.rule.id
            if filtered_.price_dependancy:
                if product.cost > filtered_.price_dependancy and filtered_.higher_percentage:
                    if filtered_.higher_percentage_unit == 1:
                        whole_sale = all_cost_price + filtered_.higher_percentage
                    else:
                        whole_sale = all_cost_price + (all_cost_price * (filtered_.higher_percentage / 100))

                    whole_sale_rule_unit = get_unit_type(filtered_.higher_percentage_unit)
                    mr = filtered_.higher_percentage
                    is_rule_applied_check_else_case = True

            if filtered_.price_dependancy2:
                if product.cost < filtered_.price_dependancy2 and filtered_.lower_percentage:
                    if filtered_.lower_percentage_unit == 1:
                        whole_sale = all_cost_price + filtered_.lower_percentage
                    else:
                        whole_sale = all_cost_price + (all_cost_price * (filtered_.lower_percentage / 100))

                    whole_sale_rule_unit = get_unit_type(filtered_.lower_percentage_unit)
                    mr = filtered_.lower_percentage
                    is_rule_applied_check_else_case = True

            if not is_rule_applied_check_else_case:
                if filtered_.percentage_unit == 1:
                    whole_sale = all_cost_price + filtered_.percentage
                else:
                    whole_sale = all_cost_price + (all_cost_price * (filtered_.percentage / 100))

                whole_sale_rule_unit = get_unit_type(filtered_.percentage_unit)
                mr = filtered_.percentage

            whole_sale = round(whole_sale, 4)
            whole_sale_rounded = round(whole_sale)

    return mr, whole_sale, whole_sale_rounded, whole_sale_rule_unit, whole_sale_rule_identity


def get_retail_margin_rule_calculation(product, all_cost_price):
    mr = 'N/A'
    whole_sale = 'N/A'
    whole_sale_rounded = 'N/A'
    whole_sale_rule_unit = 'N/A'
    whole_sale_rule_identity = 'N/A'

    if MarginRules.objects.filter(rule__rule_type=3, type=1).exists():

        categories__ = product.categories.all()

        filtered_ = MarginRules.objects.filter(type=1, product_sku=product, is_on_category=False).last()
        if not filtered_:
            filtered_ = MarginRules.objects.filter(type=1, supplier=product.supplier, is_all_categories=False,
                                                   category__in=categories__, is_on_category=True)

            if not filtered_:
                filtered_ = MarginRules.objects.filter(type=1, supplier=product.supplier, is_all_categories=True,
                                                       is_on_category=True)

            if not filtered_:
                filtered_ = MarginRules.objects.filter(type=1, is_all_suppliers=True, is_all_categories=True,
                                                       is_on_category=True)

            if filtered_:
                filtered_ = filtered_.last()

        if filtered_:
            whole_sale_rule_identity = filtered_.rule.id
            is_rule_applied_check_else_case = False
            if filtered_.price_dependancy:
                if product.cost > filtered_.price_dependancy and filtered_.higher_percentage:
                    if filtered_.higher_percentage_unit == 1:
                        whole_sale = all_cost_price + filtered_.higher_percentage
                    else:
                        whole_sale = all_cost_price + (all_cost_price * (filtered_.higher_percentage / 100))

                    whole_sale_rule_unit = get_unit_type(filtered_.higher_percentage_unit)
                    mr = filtered_.higher_percentage
                    is_rule_applied_check_else_case = True

            if filtered_.price_dependancy2:
                if product.cost < filtered_.price_dependancy2 and filtered_.lower_percentage:
                    if filtered_.lower_percentage_unit == 1:
                        whole_sale = all_cost_price + filtered_.lower_percentage
                    else:
                        whole_sale = all_cost_price + (all_cost_price * (filtered_.lower_percentage / 100))

                    whole_sale_rule_unit = get_unit_type(filtered_.lower_percentage_unit)
                    mr = filtered_.lower_percentage
                    is_rule_applied_check_else_case = True

            if not is_rule_applied_check_else_case:
                if filtered_.percentage_unit == 1:
                    whole_sale = all_cost_price + filtered_.percentage
                else:
                    whole_sale = all_cost_price + (all_cost_price * (filtered_.percentage / 100))

                whole_sale_rule_unit = get_unit_type(filtered_.percentage_unit)
                mr = filtered_.percentage

            whole_sale = round(whole_sale, 4)
            whole_sale_rounded = round(whole_sale)
            whole_sale_rounded = whole_sale_rounded - 0.01

    return mr, whole_sale, whole_sale_rounded, whole_sale_rule_unit, whole_sale_rule_identity


def calculate_price_detail_of_product(product):
    lcs, is_lcs_cost, local_cost_param_value, lcs_object = get_lcs_obj(product)
    tcs, is_tcs_cost, thenx_cost_param_value, tcs_object = get_tcs_obj(product)

    vat = 1.19
    is_vat = True

    all_cost_price = round((product.cost + lcs + tcs) * 1.19, 2)

    mr, whole_sale, whole_sale_rounded, whole_sale_rule_unit, whole_sale_rule_identity = get_margin_rule_calculation(
        product, all_cost_price)

    ret_mr, retail_price, retail_price_rounded, retail_price_rule_unit, retail_price_rule_identity = get_retail_margin_rule_calculation(
        product, all_cost_price)

    gross_profit_whole_sale = 'N/A'
    if whole_sale != 'N/A':
        gross_profit_whole_sale = round(whole_sale_rounded - all_cost_price, 2)

    gross_profit_retail_price = 'N/A'
    if retail_price != 'N/A':
        gross_profit_retail_price = round(retail_price_rounded - all_cost_price, 2)

    margin_whole_sale = 'N/A'
    if whole_sale != 'N/A':
        try:
            margin_whole_sale = round((whole_sale_rounded - all_cost_price) / whole_sale_rounded, 2)
        except:
            margin_whole_sale = 0.0

    margin_retail_price = 'N/A'
    if retail_price != 'N/A':
        try:
            margin_retail_price = round((retail_price_rounded - all_cost_price) / retail_price_rounded, 2)
        except:
            margin_retail_price = 0.0

    return {
        'local_cost': lcs,
        'local_cost_is': is_lcs_cost,
        'local_cost_param_value': local_cost_param_value,
        'lcs_object': lcs_object,

        'thenx_cost': tcs,
        'thenx_cost_is': is_tcs_cost,
        'thenx_cost_param_value': thenx_cost_param_value,
        'tcs_object': tcs_object,

        'vat': vat,
        'is_vat': is_vat,

        'all_cost_price': all_cost_price,

        'whole_sale': whole_sale,
        'whole_sale_rounded': whole_sale_rounded,
        'whole_sale_margin': mr,
        'whole_sale_rule_unit': whole_sale_rule_unit,
        'whole_sale_rule_identity': whole_sale_rule_identity,

        'retail_price': retail_price,
        'retail_price_rounded': retail_price_rounded,
        'retail_price_margin': ret_mr,
        'retail_price_rule_unit': retail_price_rule_unit,
        'retail_price_rule_identity': retail_price_rule_identity,

        'gross_profit_whole_sale': gross_profit_whole_sale,
        'margin_whole_sale': margin_whole_sale,
        'gross_profit_retail_price': gross_profit_retail_price,
        'margin_retail_price': margin_retail_price
    }


def get_job_type(type_):
    if type_ == 0:
        return "Thenx Live Product Details"
    elif type_ == 1:
        return "Processing Product Competitors Info"
    elif type_ == 2:
        return "Fetching Competitor Links"
    elif type_ == 4:
        return "Processing Product C Without Links"
    else:
        return "New Products Fetching"


def get_job_action(type_):
    if type_ == 3:
        return "Fetching"
    if type_ == 0 or type_ == 2:
        return "Import"
    else:
        return "Parser"


def get_new_products_count(new_sku):
    if new_sku == 0:
        return "N/A"
    else:
        return new_sku


def send_email_user(subject, template_name, attach_file=None, context=None):
    try:
        if context is None:
            context = {}
        text_content = render_to_string(template_name, context)
        html_content = render_to_string(template_name, context)

        email_instance = EmailMultiAlternatives(subject, text_content)
        email_instance.attach_alternative(html_content, "text/html")
        email_instance.to = [EMAIL_]

        if attach_file:
            for obj in attach_file:
                email_instance.attach_file(obj)
        email_instance.send()

    except Exception as e:
        print(e)
    return


def cron_job_logs(filename):
    _cron_logs = CronJobLogRunning.objects.all().order_by('-id')

    with open(filename, "w+") as csv_file:
        cr = csv.writer(csv_file, delimiter=",", lineterminator="\n")

        cr.writerow(['Job Name', 'Started At', 'Action', 'Scanned Sku', 'Changed Prices', 'New Sku'])
        for obj in _cron_logs:
            cr.writerow(
                [get_job_type(obj.cron_job_type), str(datetime.datetime.strftime(obj.created_at, '%Y-%m-%d %I:%M %p')),
                 get_job_action(obj.cron_job_type), get_new_products_count(obj.scanned_sku),
                 get_new_products_count(obj.changed_prices), get_new_products_count(obj.new_sku)])


def competitor_information_logs(filename):
    _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=datetime.datetime.now().date(),
                                                     is_price_change=True).order_by('id')

    with open(filename, "w+") as csv_file:
        cr = csv.writer(csv_file, delimiter=",", lineterminator="\n")
        cr.writerow(['SKU', 'Categories', 'Name', 'Thenx Position', 'Minimum Prices', 'Maximum Prices', 'Average Price',
                     'Smart Price', 'Thenx Current Price', 'Price Difference', 'Cost', 'Margin',
                     'Stock', 'Cheapest Site', 'Highest Site',
                     'Distrizone', 'Gsmnet', 'Inowgsm', 'Magazingsm', 'MokaGsm', 'PowerLaptop',
                     'Portableta', 'ServicePack'])

        for obj in _admin_logs:
            categories_ = [x.name for x in obj.product.categories.all()]
            categories_ = ','.join(categories_)

            expected_price = obj.expected_price
            if obj.expected_price == 0 or obj.expected_price == 0.0:
                expected_price = 'N/A'

            price_diff = float(obj.product_price - obj.expected_price)
            margin_diff = float(obj.product_price - obj.product_cost)
            quantity_diff = False
            if obj.product.quantity == 0:
                quantity_diff = True

            distrizone = gsmnet = inowgsm = magazingsm = mokagsm = powerlaptop = portableta = servicepack = '-'

            for obj2 in obj.competitor_site_log.all():
                if obj2.site_reference.reference_id == 1:
                    if obj2.is_error:
                        distrizone = 'In Active'
                    else:
                        distrizone = obj2.promotion_price

                if obj2.site_reference.reference_id == 2:
                    if obj2.is_error:
                        gsmnet = 'In Active'
                    else:
                        gsmnet = obj2.promotion_price

                if obj2.site_reference.reference_id == 3:
                    if obj2.is_error:
                        inowgsm = 'In Active'
                    else:
                        inowgsm = obj2.promotion_price

                if obj2.site_reference.reference_id == 4:
                    if obj2.is_error:
                        magazingsm = 'In Active'
                    else:
                        magazingsm = obj2.promotion_price

                if obj2.site_reference.reference_id == 5:
                    if obj2.is_error:
                        mokagsm = 'In Active'
                    else:
                        mokagsm = obj2.promotion_price

                if obj2.site_reference.reference_id == 6:
                    if obj2.is_error:
                        powerlaptop = 'In Active'
                    else:
                        powerlaptop = obj2.promotion_price

                if obj2.site_reference.reference_id == 7:
                    if obj2.is_error:
                        portableta = 'In Active'
                    else:
                        portableta = obj2.promotion_price

                if obj2.site_reference.reference_id == 8:
                    if obj2.is_error:
                        servicepack = 'In Active'
                    else:
                        servicepack = obj2.promotion_price

            cr.writerow([obj.product.sku, categories_, obj.product.name, obj.rank_of_product, obj.cheapest_price,
                         obj.highest_price, obj.average_price, expected_price, obj.product_price,
                         price_diff, obj.product_cost, margin_diff, quantity_diff, obj.cheapest_price_text,
                         obj.highest_price_text, distrizone, gsmnet, inowgsm, magazingsm, mokagsm,
                         powerlaptop, portableta, servicepack
                         ])


def get_competitor_links_from_server():
    url = COMPETITOR_FETCHING_LINK
    response = requests.request("GET", url)
    response = json.loads(response.content.decode("utf-8"))
    response = [{'sku': obj['productsku'], 'site_reference': obj['sitereference'], 'link': obj['link']} for obj in
                response]
    return response


def upload_competitor_info_against_product(response_list):
    new_pro = 0
    new_response_list = []
    for obj in response_list:
        try:
            site_reference = obj['site_reference']
            if site_reference == 'Protableta':
                site_reference = 'Portableta'
            prod_ = Products.objects.get(sku=obj['sku'].strip())
            competitor_id = ProductCompetitorSites.objects.filter(name__iexact=site_reference).last()
            pro, created = ProductCompetitorsLinks.objects.get_or_create(product=prod_, site_reference=competitor_id,
                                                                         link=obj['link'])
            if created:
                new_pro = new_pro + 1
            new_response_list.append(pro.id)
        except Exception as e:
            print (e)

    try:
        ProductCompetitorsLinks.objects.all().exclude(id__in=new_response_list).delete()
    except Exception as e:
        print(e)
    return new_pro


def make_updation_request(data):
    data = {"key": "TNXIEf7jzLLJXsepQGYZJ6wIPoFtrVIc", "json": data}
    url = PRICE_UPDATION_OVER_SERVER
    response = requests.request("POST", url, data=json.dumps(data))
    return response


def get_competitor_rule_reference_model(pcr):
    competitor = ''
    competitor_int = 0
    if pcr.is_all_competitors:
        competitor = 'All Competitors'
        competitor_int = 0
    else:
        if pcr.competitor:
            competitor = pcr.competitor.name
            competitor_int = pcr.competitor.id

    check_price = pcr.check_pricer
    check_price_unit = get_price_unit(pcr.check_pricer_unit)
    check_price_priority = get_price_priority(pcr.check_pricer_priority)
    competitor_priority = get_competitor_priority(pcr.competitor_priority)
    final_price_check = pcr.final_price_check
    final_price_unit = get_price_unit(pcr.final_price_unit)

    if pcr.is_all_suppliers:
        suppliers_ = 'All'
    else:
        suppliers_ = [x.name for x in pcr.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    if pcr.is_all_categories:
        categories_ = 'All'
    else:
        categories_ = [x.name for x in pcr.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if pcr.is_on_category:
        category_ = True
    if pcr.product_sku:
        product_ = pcr.product_sku.sku

    return {
        'competitor': competitor,
        'competitor_int': competitor_int,
        'check_price': check_price,
        'check_price_unit': check_price_unit,
        'check_price_unit_int': pcr.check_pricer_unit,
        'check_price_priority': check_price_priority,
        'check_price_priority_int': pcr.check_pricer_priority,
        'competitor_priority_int': pcr.competitor_priority,
        'competitor_priority': competitor_priority,
        'final_price_check': final_price_check,
        'final_price_unit': final_price_unit,
        'final_price_unit_int': pcr.final_price_unit,
        'supplier': suppliers_,
        'category': categories_,
        'is_category': category_,
        'product': product_
    }


def get_margin_rule_reference(mr):
    if mr.is_all_suppliers:
        suppliers_ = 'All'
    else:
        suppliers_ = [x.name for x in mr.supplier.all()]
        suppliers_ = ','.join(suppliers_)
    margin_type = 'Retail Price'
    name_ = 'Margin (Retail Price)'
    if mr.type == 0:
        margin_type = 'Whole Sale'
        name_ = 'Margin (Whole Sale)'
    percentage = mr.percentage
    if mr.is_all_categories:
        categories_ = 'All'
    else:
        categories_ = [x.name for x in mr.category.all()]
        categories_ = ','.join(categories_)
    category_ = False
    product_ = False
    if mr.is_on_category:
        category_ = True
    if mr.product_sku:
        product_ = mr.product_sku.sku
    return {
        'margin_type': margin_type,
        'category': categories_,
        'is_category': category_,
        'product': product_,
        'percentage': percentage,
        'supplier': suppliers_,
        'rule_type': name_,
        'percentage_unit': get_unit_type(mr.percentage_unit),
        'percentage_unit_int': mr.percentage_unit,
        'margin_type_int': mr.type
    }

