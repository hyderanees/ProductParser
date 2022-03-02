from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from .utils import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def products_new(request):
    supplier_ = category_ = product_ = None
    supplier_val = category_val = product_val = None
    limit = 500
    page = 1

    if request.method == 'POST':
        data = request.POST

        limit = int(data['limit']) if 'limit' in data else 500
        page = int(data['page']) if 'page' in data else 1

        supplier_ = int(data['supplier']) if 'supplier' in data else None
        category_ = int(data['category']) if 'category' in data else None
        product_ = data['product'] if 'product' in data else None

        supplier_val = supplier_
        category_val = category_
        product_val = product_

    if supplier_ and supplier_ != '':
        supplier_ = int(supplier_)
    else:
        supplier_ = ''
    if category_ and category_ != '':
        category_ = int(category_)
    else:
        category_ = ''

    _products = Products.objects.all().order_by('id')

    if supplier_:
        _products = _products.filter(supplier__id=supplier_)
    if category_:
        _products = _products.filter(categories__id=category_)
    if product_:
        _products = _products.filter(Q(name__icontains=product_) | Q(sku__iexact=product_))

    if supplier_ is not None or category_ is not None or product_ is not None:
        _products = _products.distinct()

    product_query_set = Paginator(_products, limit)

    try:
        product_query_set = product_query_set.page(page)
    except PageNotAnInteger:
        product_query_set = product_query_set.page(1)
    except EmptyPage:
        product_query_set = product_query_set.page(product_query_set.num_pages)

    if not product_val:
        product_val = ""

    _suppliers = Suppliers.objects.all()
    _categories = Categories.objects.all()
    return render(request, 'products/NewDesigns/products.html',
                  context={
                      'suppliers': _suppliers,
                      'categories': _categories,
                      'products': product_query_set,
                      'product_val': product_val,
                      'supplier_val': supplier_val,
                      'category_val': category_val,
                      'limit': limit,
                      'page': page
                  })


@login_required
def competitors_info_new(request):
    filter_type, filter_type2, product_sku = 0, 0, ''
    filter1, filter2, product_sku_val = 0, 0, ''
    limit = 500
    page = 1

    if request.method == 'POST':
        data = request.POST
        page = int(data['page']) if 'page' in data else 1
        limit = int(data['limit']) if 'length' in data else 500
        filter_type = int(data['filter1'])
        filter_type2 = int(data['filter2'])
        product_sku = data['product']
        filter1 = filter_type
        filter2 = filter_type2
        product_sku_val = product_sku

    if filter_type2 == 0:
        is_price_change = True
    else:
        is_price_change = False

    is_valid_ = True
    is_approved_ = False
    is_competitor_less_than_cost = False
    if filter_type == 1:
        is_competitor_less_than_cost = True
    if filter_type == 3:
        is_valid_ = False
        is_approved_ = True

    # from datetime import timedelta
    # date__ = datetime.datetime.now() - timedelta(minutes=1440*6)
    date__ = datetime.datetime.now()
    _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=date__,
                                                     is_valid=is_valid_,
                                                     is_approved=is_approved_,
                                                     is_competitor_less_than_cost=is_competitor_less_than_cost,
                                                     is_competitor_asscoiated=True).order_by('id')

    if filter_type == 4:
        _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=date__,
                                                         is_valid=is_valid_,
                                                         is_smart_price_set_applied=True,
                                                         is_approved=is_approved_,
                                                         is_competitor_asscoiated=True).order_by('id')

    if is_price_change:
        _admin_logs = _admin_logs.filter(is_price_change=True)

    if product_sku:
        _admin_logs = _admin_logs.filter(
            Q(product__name__icontains=product_sku) | Q(product__sku__iexact=product_sku))

    def extract(obj, key):
        cheapest_list = []

        is_cheapest = False
        key = key + 1
        categories_ = [x.name for x in obj.product.categories.all()]
        categories_ = ','.join(categories_)

        expected_price = round(obj.expected_price, 2)
        if obj.expected_price == 0 or obj.expected_price == 0.0:
            expected_price = 'N/A'

        is_smart_price_set_applied = False
        if obj.is_smart_price_set_applied:
            is_smart_price_set_applied = True

        old_all_cost_price = "-"
        if obj.product.old_all_cost_date:
            old_all_cost_price = str(round(obj.product.old_all_cost_price, 2)) + "-" + str(obj.product.old_all_cost_date)

        margin_neg_condition = False
        try:
            margin_ = (expected_price - obj.product.all_cost_price) / expected_price
            margin__ = round(margin_, 2)
            if margin__ < 0:
                margin_neg_condition = True
            margin_ = str(round(margin_, 2)) + " %"
        except:
            margin_ = "-"

        cheapest_list.append({'price': round(obj.product_price, 2), 'index': 0})

        dict_main = {'sr_no': key, 'sku': obj.product.sku, 'name': obj.product.name, 'categories': categories_,
                     'competitor_name': 'Thenx', 'price': round(obj.product_price,2), 'cost': obj.product_cost,
                     'margin': margin_,
                     'margin_neg_condition': margin_neg_condition,
                     'stock': '-',
                     'all_cost_price': obj.product.all_cost_price,
                     'old_all_cost_price': old_all_cost_price,
                     'id': obj.id,
                     'is_smart_price_set_applied': is_smart_price_set_applied,
                     'smart_price_set': obj.product.smart_price_value,
                     'link_status': 'active', 'last_price_date': '-', 'price_diff': '-',
                     'last_check': '-',
                     'smart_price': expected_price,
                     'is_cheapest': is_cheapest,
                     'reference_id': obj.product.reference_id,
                     'link': obj.product.url}

        competitor_details_list = []
        count_____ = 0
        count_____1 = 1
        for obj2 in obj.competitor_site_log.all():
            smart_price__ = ""
            if count_____ == 0:
                if obj.product.is_smart_price_already_set:
                    smart_price__ = obj.product.smart_price_value

            count_____ = count_____ + 1

            is_cheapest = False
            status__, last_time_date, last_time = 'active', '-', '-'
            if obj2.is_error:
                status__ = 'inactive'

            last_time = "-"

            if obj2.competitor_link:
                if obj2.old_price_date:
                    try:
                        last_time = str(round(float(obj2.old_price), 2)) + "-" + str(obj2.old_price_date)
                    except:
                        last_time = ""

            if obj2.is_error:
                promotion_price = 'N/A'
                product_cost = 'N/A'
                price_diff = 'N/A'
                stock = 'N/A'

            else:
                promotion_price = 0.0
                if obj2.promotion_price:
                    promotion_price = round(float(obj2.promotion_price), 2)
                product_cost = obj.product_cost
                stock = obj2.stock_entry
                price_diff = round(promotion_price - obj.product_price)

            site_reference_name = ''
            if obj2.site_reference:
                site_reference_name = obj2.site_reference.name

            dict_inner = {'competitor_name': site_reference_name,
                          'price': promotion_price,
                          'cost': product_cost,
                          'stock': stock,
                          'link_status': status__,
                          'last_price_date': last_time_date,
                          'price_diff': price_diff,
                          'last_check': last_time,
                          'link': obj2.link,
                          'smart_price': smart_price__,
                          'is_cheapest': is_cheapest
                          }

            proom = promotion_price
            if proom != 'N/A' and proom != 0.0:
                cheapest_list.append({'price': promotion_price, 'index': count_____1})

            count_____1 = count_____1 + 1

            competitor_details_list.append(dict_inner)

        min_index = min(cheapest_list, key=lambda x: x['price'])
        if len(cheapest_list) > 1:
            min_index_ = min_index['index']
            if min_index_ == 0:
                dict_main['is_cheapest'] = True
            else:
                competitor_details_list[min_index_ - 1]['is_cheapest'] = True

        dict_main['competitors_list'] = competitor_details_list
        return dict_main

    competitor_query_set = Paginator(_admin_logs, limit)

    try:
        competitor_query_set = competitor_query_set.page(page)
    except PageNotAnInteger:
        competitor_query_set = competitor_query_set.page(1)
    except EmptyPage:
        competitor_query_set = competitor_query_set.page(competitor_query_set.num_pages)

    competitor_query_set_ = competitor_query_set.object_list
    competitor_query_set_ = [extract(x, key) for key, x in enumerate(competitor_query_set_)]

    return render(request, 'products/NewDesigns/competitors_info.html',
                  context={
                      'competitor_query_set': competitor_query_set,
                      'competitor_query_set_': competitor_query_set_,
                      'limit': limit,
                      'page': page,
                      'filter1': filter1,
                      'filter2': filter2,
                      'product_val': product_sku_val
                  })
