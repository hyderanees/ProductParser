import io
import os
from datetime import timedelta
from .export_rules import *
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth import logout as logout_auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .add_rule import Rule
from .add_rule_csv_file import AddCSVRule
from .edit_existing_rule import EditRule
from .fetch_product_detail import FetchProductDetail
from .rules_filter import RulesFilter
from .utils import *


def login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email'] if 'email' in request.POST else ''
        password = request.POST['password'] if 'password' in request.POST else ''
        email = email.lower().strip()
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active:
                login_auth(request, user)
                return redirect('products:home')
        context = {'error': 'Email or Password is wrong'}
    return render(request, 'products/login.html', context=context)


def logout(request):
    logout_auth(request)
    return redirect('login')


def home(request):
    competitor_count = ProductCompetitorSites.objects.count()
    competitor_link = ProductCompetitorsLinks.objects.count()
    total_brands = Brands.objects.count()
    total_suppliers = Suppliers.objects.count()
    total_categories = Categories.objects.count()
    total_products = Products.objects.count()

    rules_info = Rules.objects.aggregate(
        margin_rules=Count('pk', filter=Q(rule_type=3)),
        warranty_rules=Count('pk', filter=Q(rule_type=1)),
        local_cost_rules=Count('pk', filter=Q(rule_type=4)),
        thenx_cost_rules=Count('pk', filter=Q(rule_type=5)),
        competitor_rules=Count('pk', filter=Q(rule_type=6)),
        total_rules=Count('pk')
    )

    total_rules = rules_info['total_rules']
    margin_rules = rules_info['margin_rules']
    warranty_rules = rules_info['warranty_rules']
    local_cost_rules = rules_info['local_cost_rules']
    thenx_cost_rules = rules_info['thenx_cost_rules']
    competitor_rules = rules_info['competitor_rules']

    rank_information = AdminLogOfJobToShow.objects.filter(created_at__date=datetime.datetime.now().date()).aggregate(
        same_prices=Count('pk', filter=Q(price_change_effect=1)),
        exceeded_prices=Count('pk', filter=Q(price_change_effect=2)),
        decreased_prices=Count('pk', filter=Q(price_change_effect=3)),
        total_prices=Count('pk', filter=Q(price_change_effect__in=[1, 2, 3])),
        updated_prices=Count('pk', filter=Q(is_approved=True)),
        is_competitor_rule_applied=Count('pk', filter=Q(is_competitor_rule_applied=True)),
        is_margin_rule_applied=Count('pk', filter=Q(is_margin_rule_applied=True)),
        is_original_price_applied=Count('pk', filter=Q(is_original_price_applied=True))
    )

    total_prices = rank_information['total_prices']
    same_prices = rank_information['same_prices']
    exceeded_prices = rank_information['exceeded_prices']
    decreased_prices = rank_information['decreased_prices']
    updated_prices = rank_information['updated_prices']
    is_competitor_rule_applied = rank_information['is_competitor_rule_applied']
    is_margin_rule_applied = rank_information['is_margin_rule_applied']
    is_original_price_applied = rank_information['is_original_price_applied']

    crons_info = ProductCompetitorSitesReference.objects.filter(
        created_at__date=datetime.datetime.now().date()).aggregate(
        total_crons=Count('pk'),
        succeded_crons=Count('pk', filter=Q(is_error=False)),
        failure_crons=Count('pk', filter=Q(is_error=True))
    )

    total_crons = crons_info['total_crons']
    succeded_crons = crons_info['succeded_crons']
    failure_crons = crons_info['failure_crons']

    weekly_new_products = WeeklyReportNewProducts.objects.all().last()

    context = {'competitor_count': competitor_count, 'competitor_link': competitor_link, 'total_brands': total_brands,
               'total_suppliers': total_suppliers, 'total_categories': total_categories,
               'total_products': total_products, 'total_rules': total_rules, 'margin_rules': margin_rules,
               'warranty_rules': warranty_rules, 'local_cost_rules': local_cost_rules,
               'thenx_cost_rules': thenx_cost_rules,
               'competitor_rules': competitor_rules, 'total_crons': total_crons, 'failure_crons': failure_crons,
               'succeded_crons': succeded_crons, 'total_prices': total_prices, 'exceeded_prices': exceeded_prices,
               'same_prices': same_prices, 'decreased_prices': decreased_prices, 'updated_prices': updated_prices,
               'is_competitor_rule_applied': is_competitor_rule_applied,
               'is_margin_rule_applied': is_margin_rule_applied,
               'is_original_price_applied': is_original_price_applied,
               'weekly_new_products': weekly_new_products
               }
    return render(request, 'products/dashboard.html', context=context)


@login_required
def products(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        supplier_ = request.POST['supplier']
        category_ = request.POST['category']
        product_ = request.POST['product']

        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        if supplier_ and supplier_ != 'select':
            supplier_ = int(supplier_)
        else:
            supplier_ = ''
        if category_ and category_ != 'select':
            category_ = int(category_)
        else:
            category_ = ''

        _products = Products.objects.all().order_by('id')
        # if search_parameter: _products = Products.objects.filter(Q(name__icontains=search_parameter) | Q(
        # sku__icontains=search_parameter) | Q(brand__name__icontains=search_parameter) | Q(
        # supplier__name__icontains=search_parameter) | Q(categories__name__icontains=search_parameter) ).order_by(
        # 'id') _products = _products.distinct()

        if supplier_:
            _products = _products.filter(supplier__id=supplier_)
        if category_:
            _products = _products.filter(categories__id=category_)
        if product_:
            _products = _products.filter(Q(name__icontains=product_) | Q(sku__icontains=product_))

        if supplier_ is not None or category_ is not None or product_ is not None:
            _products = _products.distinct()

        def extract(obj, key):
            categories_ = [x.name for x in obj.categories.all()]
            categories_ = ','.join(categories_)

            supplier_ = 'N/A'
            if obj.supplier:
                supplier_ = obj.supplier.name

            # pci = ProductCalculationInformation.objects.filter(product=obj).last()
            # if pci:
            #     local_cost_supplier = pci.local_cost_supplier
            #     thenx_cost_supplier = pci.thenx_cost_supplier
            #     vat = pci.vat
            #     all_cost_price = pci.all_cost_price
            #     whole_sale_price = pci.whole_sale_price
            #     gross_profit_whole_sale = pci.gross_profit_whole_sale
            #     retail_sale_price = pci.retail_sale_price
            #     gross_profit_retail_sale = pci.gross_profit_retail_sale
            #     whole_sale_margin = pci.whole_sale_margin
            #     retail_margin = pci.retail_margin
            #     old_price_all_cost = 'N/A'
            #     last_update = str(pci.created_at)
            # else:
            response_ = calculate_price_detail_of_product(obj)
            smart_price_set = 'N/A'
            if obj.is_smart_price_already_set:
                smart_price_set = obj.smart_price_value

            local_cost_supplier = response_['local_cost']
            local_cost_supplier_check = response_['local_cost_is']
            if local_cost_supplier_check != 'N/A':
                local_cost_supplier = round(local_cost_supplier, 2)
            else:
                local_cost_supplier = 'N/A'

            thenx_cost_supplier = response_['thenx_cost']
            thenx_cost_supplier_check = response_['thenx_cost_is']
            if thenx_cost_supplier_check != 'N/A':
                thenx_cost_supplier = round(thenx_cost_supplier, 2)
            else:
                thenx_cost_supplier = 'N/A'

            vat = response_['vat']
            if vat and vat != 'N/A':
                vat = round(vat, 2)

            all_cost_price = response_['all_cost_price']
            if all_cost_price and all_cost_price != 'N/A':
                all_cost_price = round(all_cost_price, 2)

            whole_sale_price = response_['whole_sale_rounded']
            gross_profit_whole_sale = response_['gross_profit_whole_sale']
            gross_profit_whole_sale_margin = response_['margin_whole_sale']
            whole_sale_margin = response_['whole_sale_margin']
            whole_sale_rule_unit = response_['whole_sale_rule_unit']

            retail_sale_price = response_['retail_price_rounded']
            gross_profit_retail_sale = response_['gross_profit_retail_price']
            gross_profit_retail_sale_margin = response_['margin_retail_price']
            retail_margin = response_['retail_price_margin']
            retail_price_rule_unit = response_['retail_price_rule_unit']

            old_price_all_cost = 'N/A'
            last_update = 'N/A'

            is_smart_price_set_applied = 'No'
            if obj.is_smart_price_already_set:
                is_smart_price_set_applied = 'Yes'

            return {
                'name': obj.name,
                'sr_no': key,
                'is_smart_price_set_applied': is_smart_price_set_applied,
                'smart_price_set': smart_price_set,
                'vat': vat,
                'reference_id': obj.reference_id,
                'sku': obj.sku,
                'supplier_price': obj.cost,
                'categories': categories_,
                'supplier': supplier_,
                'local_cost': local_cost_supplier,
                'thenx_cost': thenx_cost_supplier,
                'all_cost': all_cost_price,
                'margin_wholesale': whole_sale_margin,
                'margin_retail': retail_margin,
                'whole_sale_price': whole_sale_price,
                'retail_price': retail_sale_price,
                'g_profile_wholesale': gross_profit_whole_sale,
                'g_profile_retail': gross_profit_retail_sale,
                'g_profile_wholesale_margin': gross_profit_whole_sale_margin,
                'g_profile_retail_margin': gross_profit_retail_sale_margin,
                'whole_sale_rule_unit': whole_sale_rule_unit,
                'retail_price_rule_unit': retail_price_rule_unit,
                'last_update': last_update,
                'old_price_all_cost': old_price_all_cost
            }

        items = paginate(_products, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)

    _suppliers = Suppliers.objects.all()
    _categories = Categories.objects.all()
    return render(request, 'products/products_new.html', context={'suppliers': _suppliers,
                                                                  'categories': _categories})


@login_required
def scrapping_job_links(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        filter_ = request.POST['filter']
        competitor_ = request.POST['competitorsite']
        product_ = request.POST['product']

        filter__ = None
        if filter_ and filter_ != '0':
            filter_ = int(filter_)
            if filter_ == 1:
                filter__ = True
            else:
                filter__ = False
        else:
            filter_ = ''

        if competitor_ and competitor_ != '0':
            competitor_ = int(competitor_)
        else:
            competitor_ = ''

        jobs_info_ = ProductCompetitorSitesReference.objects.filter(created_at__date=datetime.datetime.now().date())

        if filter_:
            jobs_info_ = jobs_info_.filter(is_error=filter__)

        if competitor_:
            jobs_info_ = jobs_info_.filter(site_reference__id=competitor_)

        if product_:
            jobs_info_ = jobs_info_.filter(Q(product__name__icontains=product_) | Q(product__sku__icontains=product_))

        if filter_ is not None or product_ is not None:
            jobs_info_ = jobs_info_.distinct()

        def extract(obj, key):
            categories_ = [x.name for x in obj.product.categories.all()]
            categories_ = ','.join(categories_)

            competitor_link_identity = 0
            if obj.competitor_link:
                competitor_link_identity = obj.competitor_link.id

            supplier_ = 'N/A'
            if obj.product.supplier:
                supplier_ = obj.product.supplier.name

            response_ = calculate_price_detail_of_product(obj.product)
            smart_price_set = 'N/A'
            if obj.product.is_smart_price_already_set:
                smart_price_set = obj.product.smart_price_value

            all_cost_price = response_['all_cost_price']
            if all_cost_price and all_cost_price != 'N/A':
                all_cost_price = round(all_cost_price, 2)

            is_smart_price_set_applied = 'No'
            if obj.product.is_smart_price_already_set:
                is_smart_price_set_applied = 'Yes'

            job_status = 'Succeeded'
            if obj.is_error:
                job_status = 'Fail'

            if obj.is_error:
                promotion_price = 'N/A'

            else:
                promotion_price = 0.0
                if obj.promotion_price:
                    promotion_price = float(obj.promotion_price)

            site_reference_name = ''
            if obj.site_reference:
                site_reference_name = obj.site_reference.name

            return {
                'name': obj.product.name,
                'sr_no': key,
                'is_smart_price_set_applied': is_smart_price_set_applied,
                'smart_price_set': smart_price_set,
                'reference_id': obj.product.reference_id,
                'sku': obj.product.sku,
                'categories': categories_,
                'supplier': supplier_,
                'all_cost': all_cost_price,
                'job_status': job_status,
                'price_fetched': promotion_price,
                'error_detail': obj.error_information,
                'site_reference_name': site_reference_name,
                'site_reference_link': obj.link,
                'competitor_link_identity': competitor_link_identity
            }

        items = paginate(jobs_info_, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)

    competitor_sites = ProductCompetitorSites.objects.all()
    return render(request, 'products/scrapping_jobs.html', context={'competitor_sites': competitor_sites})


@login_required
def product_detail(request, product_id):
    # ProductCompetitorsLinks.objects.all().delete()
    # ProductCompetitorSites.objects.all().delete()
    ProductCompetitorSites.objects.get_or_create(reference_id=1, name='Distrizone')
    ProductCompetitorSites.objects.get_or_create(reference_id=2, name='Gsmnet')
    ProductCompetitorSites.objects.get_or_create(reference_id=3, name='Inowgsm')
    ProductCompetitorSites.objects.get_or_create(reference_id=4, name='Magazingsm')
    ProductCompetitorSites.objects.get_or_create(reference_id=5, name='MokaGsm')
    ProductCompetitorSites.objects.get_or_create(reference_id=6, name='PowerLaptop')
    ProductCompetitorSites.objects.get_or_create(reference_id=7, name='Portableta')
    ProductCompetitorSites.objects.get_or_create(reference_id=8, name='ServicePack')
    ProductCompetitorSites.objects.get_or_create(reference_id=9, name='sepmobile')
    ProductCompetitorSites.objects.get_or_create(reference_id=10, name='sunnex')
    ProductCompetitorSites.objects.get_or_create(reference_id=11, name='connectshop')
    ProductCompetitorSites.objects.get_or_create(reference_id=12, name='tradegsm')
    product = Products.objects.get(id=product_id)
    context = {'product': product,
               'product_competitors': ProductCompetitorSites.objects.all(),
               'competitors': ProductCompetitorsLinks.objects.filter(product=product),
               'pro': calculate_price_detail_of_product(product)}
    return render(request, 'products/product_detail/product_detail.html', context=context)


@login_required
def add_product_competitor(request):
    data = request.POST
    competitor_id = int(data['competitor_id'])
    competitor_link = data['competitor_link']
    product_id = int(data['product_id'])

    product_id = Products.objects.get(id=product_id)
    competitor_id = ProductCompetitorSites.objects.get(id=competitor_id)
    ProductCompetitorsLinks.objects.create(product=product_id, site_reference=competitor_id, link=competitor_link)

    pc = ProductCompetitorsLinks.objects.filter(product=product_id)
    pc = [{'id': x.id, 'sitename': x.site_reference.name, 'sitelink': x.link} for x in pc]

    return JsonResponse(data=pc, safe=False)


@login_required
def delete_product_competitor(request):
    data = request.POST
    link_id = int(data['id'])
    ProductCompetitorsLinks.objects.get(id=link_id).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_competitor_info(request):
    data = json.loads(request.body.decode('utf-8'))
    ids_array = data['idsArray']
    ids_array = [int(x) for x in ids_array]

    AdminLogOfJobToShow.objects.filter(id__in=ids_array).update(is_valid=False)

    return JsonResponse(data={'success': True}, safe=False)


@login_required
def update_products_smart_price_info(request):
    data = json.loads(request.body.decode('utf-8'))
    ids_array = data['idsArray']
    ids_array = [int(x) for x in ids_array]

    list_ = []
    is_smart_price_found_ = False
    for obj in ids_array:
        prod = Products.objects.get(reference_id=obj)
        response_ = calculate_price_detail_of_product(prod)
        cost__ = response_['all_cost_price']
        if prod.smart_price_value != 0 or prod.smart_price_value != 0.0:
            competitor = 'N/A'
            is_smart_price_found_ = True

            dict_ = {'sku': str(prod.sku), 'price': prod.smart_price_value, 'alias': competitor,
                     'cost': cost__}
            list_.append(dict_)

    make_updation_request(list_)
    return JsonResponse(data={'success': True, 'is_smart_price_found': is_smart_price_found_}, safe=False)


@login_required
def delete_products_info(request):
    data = json.loads(request.body.decode('utf-8'))
    ids_array = data['idsArray']
    ids_array = [int(x) for x in ids_array]

    ids_array = Products.objects.filter(id__in=ids_array)
    wr_ = WarrantyRule.objects.filter(product_sku__in=ids_array)
    mr_ = MarginRules.objects.filter(product_sku__in=ids_array)
    lc_ = LocalCostSupplier.objects.filter(product_sku__in=ids_array)
    tc_ = ThenxCostSupplier.objects.filter(product_sku__in=ids_array)
    pcr_ = PriceCompetitorRule.objects.filter(product_sku__in=ids_array)
    ProductCompetitorSitesReference.objects.filter(product__in=ids_array).delete()
    AdminLogOfJobToShow.objects.filter(product__in=ids_array).delete()
    ProductCompetitorsLinks.objects.filter(product__in=ids_array).delete()
    rules1_ = [x.rule.id for x in wr_]
    rules2_ = [x.rule.id for x in mr_]
    rules3_ = [x.rule.id for x in lc_]
    rules4_ = [x.rule.id for x in tc_]
    rules5_ = [x.rule.id for x in pcr_]
    rules__ = rules1_ + rules2_ + rules3_ + rules4_ + rules5_
    Rules.objects.filter(id__in=rules__).delete()
    ids_array.delete()

    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_scrapping_links(request):
    data = json.loads(request.body.decode('utf-8'))
    ids_array = data['idsArray']
    ids_array = [int(x) for x in ids_array]

    for obj in ids_array:
        if obj != 0:
            ProductCompetitorsLinks.objects.filter(id=obj).delete()

    return JsonResponse(data={'success': True}, safe=False)


@login_required
def update_competitor_info(request):
    data = json.loads(request.body.decode('utf-8'))
    ids_array = data['idsArray']
    ids_array = [int(x) for x in ids_array]

    list_ = []
    for obj in ids_array:
        alojt = AdminLogOfJobToShow.objects.get(id=obj)
        if alojt.expected_price != 0 or alojt.expected_price != 0.0:
            alojt.is_approved = True
            alojt.is_valid = False
            alojt.updated_time = datetime.datetime.now()

            competitor = alojt.competitor_site_log.all()
            if competitor:
                try:
                    competitor = competitor[0].site_reference.name
                except:
                    competitor = 'N/A'
            else:
                competitor = 'N/A'

            dict_ = {'sku': str(alojt.product.sku), 'price': alojt.expected_price, 'alias': competitor,
                     'cost': alojt.all_cost_price}
            list_.append(dict_)
            alojt.save()

    make_updation_request(list_)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def update_all_competitor_info(request):
    list_ = []

    data = json.loads(request.body.decode('utf-8'))
    filter_type = int(data['filter_type'])
    filter_type2 = int(data['filter_type2'])

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

    _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=datetime.datetime.now().date(),
                                                     is_valid=is_valid_,
                                                     is_approved=is_approved_,
                                                     is_competitor_less_than_cost=is_competitor_less_than_cost,
                                                     is_competitor_asscoiated=True).order_by('id')

    if filter_type == 4:
        _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=datetime.datetime.now().date(),
                                                         is_valid=is_valid_,
                                                         is_smart_price_set_applied=True,
                                                         is_approved=is_approved_,
                                                         is_competitor_asscoiated=True).order_by('id')

    if is_price_change:
        _admin_logs = _admin_logs.filter(is_price_change=True)

    # _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=datetime.datetime.now().date(),
    #                                                  is_valid=True,
    #                                                  is_competitor_less_than_cost=False,
    #                                                  is_competitor_asscoiated=True,
    #                                                  is_price_change=True)
    for alojt in _admin_logs:
        if alojt.expected_price != 0 or alojt.expected_price != 0.0:
            alojt.is_approved = True
            alojt.is_valid = False
            alojt.updated_time = datetime.datetime.now()

            competitor = alojt.competitor_site_log.all()
            if competitor:
                try:
                    competitor = competitor[0].site_reference.name
                except:
                    competitor = 'N/A'
            else:
                competitor = 'N/A'

            dict_ = {'sku': str(alojt.product.sku), 'price': alojt.expected_price, 'alias': competitor,
                     'cost': alojt.all_cost_price}
            list_.append(dict_)
            alojt.save()

    make_updation_request(list_)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def update_all_daily_report(request):
    list_ = []

    # _admin_logs = AdminLogOfJobToShow.objects.filter(
    #     created_at__date=datetime.datetime.now().date(),
    #     is_valid=True)

    data = json.loads(request.body.decode('utf-8'))

    rule_applied = data['rule_applied']
    price_applied = data['price_applied']
    product_ = data['product']

    if rule_applied and rule_applied != 'select':
        rule_applied = int(rule_applied)
    else:
        rule_applied = 0
    if price_applied and price_applied != 'select':
        price_applied = int(price_applied)
    else:
        price_applied = 0

    is_approved_check = False
    is_valid = True
    if rule_applied == 4:
        is_approved_check = True
        is_valid = False

    _admin_logs = AdminLogOfJobToShow.objects.filter(
        created_at__date=datetime.datetime.now().date(),
        is_approved=is_approved_check,
        is_valid=is_valid).order_by('-id')

    if rule_applied != 0:
        if rule_applied == 1:
            _admin_logs = _admin_logs.filter(is_margin_rule_applied=True)
        elif rule_applied == 2:
            _admin_logs = _admin_logs.filter(is_competitor_rule_applied=True)
        elif rule_applied == 3:
            _admin_logs = _admin_logs.filter(is_original_price_applied=True)

    if price_applied != 0:
        if price_applied == 1:
            _admin_logs = _admin_logs.filter(price_change_effect=1)
        elif price_applied == 2:
            _admin_logs = _admin_logs.filter(price_change_effect=2)
        elif price_applied == 3:
            _admin_logs = _admin_logs.filter(price_change_effect=3)

    if rule_applied == 5:
        _admin_logs = AdminLogOfJobToShow.objects.filter(
            created_at__date=datetime.datetime.now().date(),
            is_competitor_less_than_cost=True,
            is_valid=is_valid).order_by('-id')

    if product_:
        _admin_logs = AdminLogOfJobToShow.objects.filter(
            Q(product__name__icontains=product_) | Q(product__sku__icontains=product_)).filter(
            created_at__date=datetime.datetime.now().date(),
            is_approved=is_approved_check,
            is_valid=is_valid)

    if rule_applied is not None or price_applied is not None or product_ is not None:
        _admin_logs = _admin_logs.distinct()

    for alojt in _admin_logs:
        if alojt.expected_price != 0 or alojt.expected_price != 0.0:
            alojt.is_approved = True
            alojt.is_valid = False
            alojt.updated_time = datetime.datetime.now()

            competitor = alojt.competitor_site_log.all()
            if competitor:
                try:
                    competitor = competitor[0].site_reference.name
                except:
                    competitor = 'N/A'
            else:
                competitor = 'N/A'

            dict_ = {'sku': str(alojt.product.sku), 'price': alojt.expected_price, 'alias': competitor,
                     'cost': alojt.all_cost_price}
            list_.append(dict_)
            alojt.save()

    make_updation_request(list_)
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def update_smart_price(request):
    data = json.loads(request.body.decode('utf-8'))
    sid = int(data['sid'])
    sprice = data['sPrice']

    admin_ = AdminLogOfJobToShow.objects.get(id=sid)

    if sprice == 0 or sprice == 0.0 or sprice == '0' or sprice == '0.0':
        prod = admin_.product
        prod.is_smart_price_already_set = False
        prod.smart_price_value = 0
        prod.save()

    else:

        admin_ = AdminLogOfJobToShow.objects.get(id=sid)
        admin_.expected_price = sprice
        admin_.save()

        prod = admin_.product
        prod.is_smart_price_already_set = True
        prod.smart_price_value = sprice
        prod.save()

    return JsonResponse(data={'succes': True}, safe=False)


@login_required
def update_smart_price_of_product(request):
    data = json.loads(request.body.decode('utf-8'))
    sid = int(data['sid'])
    sprice = data['sPrice']

    prod = Products.objects.get(id=sid)

    if sprice == 0 or sprice == 0.0 or sprice == '0' or sprice == '0.0':
        prod.is_smart_price_already_set = False
        prod.smart_price_value = 0
        prod.save()

    else:
        prod.is_smart_price_already_set = True
        prod.smart_price_value = sprice
        prod.save()

    return JsonResponse(data={'success': True}, safe=False)


@login_required
def fetch_product_details(request):
    data = request.POST
    product_id = int(data['id'])
    product = Products.objects.get(id=product_id)
    pcl = ProductCompetitorsLinks.objects.filter(product=product)
    fetching_details = FetchProductDetail(pcl)
    fetching_details.iterate_over_query_set()
    fetching_details = fetching_details.return_final_response()
    return JsonResponse(data=fetching_details, safe=False)


@login_required
def fetch_testing_info(request):
    from .product_competitor_job import product_competitor_job
    product_competitor_job()
    return JsonResponse(data={}, safe=False)


@login_required
def categories(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        _categories = Categories.objects.all().order_by('id')
        if search_parameter:
            _categories = Categories.objects.filter(name__icontains=search_parameter).order_by('id')

        def extract(obj, key):
            return {
                'sr_no': key,
                'name': obj.name,
                'reference_id': obj.reference_id,
                'total_products': Products.objects.filter(categories=obj).count()
            }

        items = paginate(_categories, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/categories.html', context={})


@login_required
def brands(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        _brand = Brands.objects.all().order_by('id')
        if search_parameter:
            _brand = Brands.objects.filter(name__icontains=search_parameter).order_by('id')

        def extract(obj, key):
            return {
                'sr_no': key,
                'name': obj.name,
                'reference_id': obj.reference_id,
                'total_products': Products.objects.filter(brand=obj).count()
            }

        items = paginate(_brand, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/brands.html', context={})


@login_required
def all_competitors_info(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 10

        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        _admin_logs = AdminLogOfJobToShow.objects.filter(is_valid=True, is_competitor_asscoiated=True).order_by('id')
        if search_parameter:
            _admin_logs = AdminLogOfJobToShow.objects.filter(name__icontains=search_parameter, is_valid=True,
                                                             is_competitor_asscoiated=True).order_by(
                'id')

        def get_date_time_from_datetime(obj):
            return datetime.datetime.strftime(obj, '%d-%m-%Y %H:%M')

        def get_date_from_datetime(obj):
            return datetime.datetime.strftime(obj, '%d-%m-%Y')

        def extract(obj, key):
            competitor_link_list = []
            categories_ = [x.name for x in obj.product.categories.all()]
            categories_ = ','.join(categories_)

            expected_price = obj.expected_price
            if obj.expected_price == 0 or obj.expected_price == 0.0:
                expected_price = 'N/A'

            dict_main = {'sr_no': key, 'sku': obj.product.sku, 'name': obj.product.name, 'categories': categories_,
                         'competitor_name': 'Thenx', 'price': obj.product_price, 'cost': obj.product_cost,
                         'margin': '-',
                         'stock': '-',
                         'link_status': 'Active', 'last_price_date': '-', 'price_diff': '-',
                         'last_check': get_date_time_from_datetime(obj.product.updated_at),
                         'smart_price': expected_price,
                         'id': obj.id,
                         'link': obj.product.url}
            competitor_link_list.append(dict_main)

            for obj2 in obj.competitor_site_log.all():
                status__, last_time_date, last_time = 'Active', '-', '-'
                if obj2.is_error:
                    status__ = 'InActive'

                if obj2.competitor_link:
                    last_time_update = ProductCompetitorSitesReference.objects.filter(
                        competitor_link=obj2.competitor_link).order_by('-id')
                    if last_time_update.count() > 2:
                        last_time_update = last_time_update[1]
                        last_time_date = str(last_time_update.promotion_price) + '/' + get_date_from_datetime(
                            last_time_update.created_at)
                        last_time = get_date_time_from_datetime(last_time_update.created_at)

                if obj2.is_error:
                    promotion_price = 'N/A'
                    product_cost = 'N/A'
                    price_diff = 'N/A'
                    stock = 'N/A'

                else:
                    promotion_price = 0.0
                    if obj2.promotion_price:
                        promotion_price = float(obj2.promotion_price)
                    product_cost = obj.product_cost
                    stock = obj2.stock_entry
                    price_diff = round(promotion_price - obj.product_price)

                site_reference_name = ''
                if obj2.site_reference:
                    site_reference_name = obj2.site_reference.name

                dict_inner = {'sr_no': '', 'sku': '', 'name': '', 'categories': '',
                              'competitor_name': site_reference_name, 'price': promotion_price,
                              'cost': product_cost,
                              'margin': '-', 'stock': stock,
                              'link_status': status__, 'last_price_date': last_time_date,
                              'price_diff': price_diff,
                              'last_check': last_time,
                              'smart_price': '',
                              'link': obj2.link}
                competitor_link_list.append(dict_inner)
            competitor_link_list.append({'sr_no': '', 'sku': '', 'name': '', 'categories': '',
                                         'competitor_name': '', 'price': '',
                                         'cost': '',
                                         'margin': '', 'stock': '',
                                         'link_status': '', 'last_price_date': '',
                                         'price_diff': '',
                                         'smart_price': '',
                                         'last_check': '',
                                         'link': ''})
            return competitor_link_list

        items = paginate(_admin_logs, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/all_competitors_info.html', context={})


@login_required
def updated_on_thenx(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 10

        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        _admin_logs = AdminLogOfJobToShow.objects.filter(is_approved=True,
                                                         created_at__date=datetime.datetime.now().date(), ).order_by(
            '-updated_time')
        if search_parameter:
            _admin_logs = AdminLogOfJobToShow.objects.filter(name__icontains=search_parameter,
                                                             created_at__date=datetime.datetime.now().date(),
                                                             is_approved=True).order_by(
                '-updated_time')

        def get_date_time_from_datetime(obj):
            return datetime.datetime.strftime(obj, '%d-%m-%Y %H:%M')

        def get_date_from_datetime(obj):
            return datetime.datetime.strftime(obj, '%d-%m-%Y')

        def extract(obj, key):
            categories_ = [x.name for x in obj.product.categories.all()]
            categories_ = ','.join(categories_)

            expected_price = obj.expected_price
            if obj.expected_price == 0 or obj.expected_price == 0.0:
                expected_price = 'N/A'

            dict_main = {'sr_no': key, 'sku': obj.product.sku, 'name': obj.product.name, 'categories': categories_,
                         'price': obj.product_price, 'cost': obj.product_cost,
                         'updated_at': get_date_time_from_datetime(obj.updated_time),
                         'smart_price': expected_price,
                         'id': obj.id,
                         'all_cost_price': obj.all_cost_price,
                         'thenx_link': obj.product.url}
            return dict_main

        items = paginate(_admin_logs, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/thenx_active_info.html', context={})


@login_required
def send_email(request):
    current_date = datetime.datetime.now()
    _admin_logs = AdminLogOfJobToShow.objects.filter(created_at__date=current_date.date(),
                                                     is_price_change=True).order_by('id')

    competitors_email = []
    for obj in _admin_logs:
        expected_price_ = obj.expected_price
        if obj.expected_price == 0 or obj.expected_price == 0.0:
            expected_price_ = 'N/A'

        dict_ = {'product_name': obj.product.name, 'sku': obj.product_sku, 'expected_price': expected_price_,
                 'price': obj.product_price}
        compet_ = []
        for obj2 in obj.competitor_site_log.all():
            name_ = ''
            if obj2.site_reference:
                name_ = obj2.site_reference.name
            elif obj2.competitor_link:
                if obj2.competitor_link.site_reference:
                    name_ = obj2.competitor_link.site_reference

            old_price_ = obj2.old_price
            price_diff = 'N/A'
            if obj2.old_price == '0' or obj2.old_price == '0.0' or obj2.old_price == '':
                old_price_ = 'N/A'
            else:
                try:
                    price_diff = float(old_price_) - float(obj2.promotion_price)
                except:
                    price_diff = 'N/A'

            status__ = True
            if obj2.is_error:
                status__ = False
            compet_.append({'name': name_, 'old_price': old_price_, 'current_price': obj2.promotion_price,
                            'stock': obj2.stock_entry,
                            'price_diff': price_diff, 'status': status__})
        dict_['competitors'] = compet_
        competitors_email.append(dict_)
    return render(request, 'products/email_templates/daily_update_mail.html',
                  context={'competitors_email': competitors_email,
                           'date': datetime.datetime.strftime(current_date, '%d %b, %Y'),
                           'product_change': len(competitors_email)})


@login_required
def daily_update(request):
    # AdminLogOfJobToShow.objects.filter(
    #     created_at__date=datetime.datetime.now().date()).delete()
    # ProductCompetitorSitesReference.objects.filter(
    #     created_at__date=datetime.datetime.now().date()).delete()
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 10

        rule_applied = request.POST['rule_applied']
        price_applied = request.POST['price_applied']
        product_ = request.POST['product']

        if rule_applied and rule_applied != 'select':
            rule_applied = int(rule_applied)
        else:
            rule_applied = 0
        if price_applied and price_applied != 'select':
            price_applied = int(price_applied)
        else:
            price_applied = 0

        is_approved_check = False
        is_valid = True
        if rule_applied == 4:
            is_approved_check = True
            is_valid = False

        _admin_logs = AdminLogOfJobToShow.objects.filter(
            created_at__date=datetime.datetime.now().date(),
            is_approved=is_approved_check,
            is_valid=is_valid).order_by('-id')

        if rule_applied != 0:
            if rule_applied == 1:
                _admin_logs = _admin_logs.filter(is_margin_rule_applied=True)
            elif rule_applied == 2:
                _admin_logs = _admin_logs.filter(is_competitor_rule_applied=True)
            elif rule_applied == 3:
                _admin_logs = _admin_logs.filter(is_original_price_applied=True)

        if price_applied != 0:
            if price_applied == 1:
                _admin_logs = _admin_logs.filter(price_change_effect=1)
            elif price_applied == 2:
                _admin_logs = _admin_logs.filter(price_change_effect=2)
            elif price_applied == 3:
                _admin_logs = _admin_logs.filter(price_change_effect=3)

        if rule_applied == 5:
            _admin_logs = AdminLogOfJobToShow.objects.filter(
                created_at__date=datetime.datetime.now().date(),
                is_competitor_less_than_cost=True,
                is_valid=is_valid).order_by('-id')

        if product_:
            _admin_logs = AdminLogOfJobToShow.objects.filter(
                Q(product__name__icontains=product_) | Q(product__sku__icontains=product_)).filter(
                created_at__date=datetime.datetime.now().date(),
                is_approved=is_approved_check,
                is_valid=is_valid)

        if rule_applied is not None or price_applied is not None or product_ is not None:
            _admin_logs = _admin_logs.distinct()

        def get_bool_value(val):
            if val:
                return "YES"
            return "NO"

        def extract(obj, key):
            expected_price = obj.expected_price
            price_diff = 'N/A'
            if obj.expected_price == 0 or obj.expected_price == 0.0:
                expected_price = 'N/A'
            else:
                price_diff = round(expected_price - obj.product_price, 2)
                if price_diff == 0 or price_diff == 0.0:
                    price_diff = 'N/A'

            categories_ = [x.name for x in obj.product.categories.all()]
            categories_ = ','.join(categories_)

            supplier_ = 'N/A'
            if obj.product.supplier:
                supplier_ = obj.product.supplier.name

            mr_detail = {}
            cr_detail = {}

            if obj.margin_rule_identity:
                mr_detail = get_margin_rule_reference(obj.margin_rule_identity)
            if obj.competitor_rule_identity:
                cr_detail = get_competitor_rule_reference_model(obj.competitor_rule_identity)

            is_smart_price_set_applied = 'No'
            if obj.is_smart_price_set_applied:
                is_smart_price_set_applied = 'Yes'

            dict_main = {'sr_no': key, 'sku': obj.product.sku, 'name': obj.product.name, 'categories': categories_,
                         'supplier': supplier_, 'price': obj.product_price, 'cost': obj.product_cost,
                         'is_margin_rule': get_bool_value(obj.is_margin_rule_applied),
                         'is_original_price_applied': get_bool_value(obj.is_original_price_applied),
                         'is_competitor_rule_applied': get_bool_value(obj.is_competitor_rule_applied),
                         'cr_detail': cr_detail,
                         'mr_detail': mr_detail,
                         'id': obj.id,
                         'is_smart_price_set_applied': is_smart_price_set_applied,
                         'all_cost_price': obj.all_cost_price,
                         'product_id': obj.product.reference_id,
                         'price_diff': price_diff,
                         'smart_price': expected_price}
            return dict_main

        items = paginate(_admin_logs, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/daily_update.html', context={})


@login_required
def instant_push(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 10

        job_logs_ = InstantJobDeclaration.objects.all().order_by('-id')

        def get_job_status(val):
            if val == 1:
                return "Completed"
            return "InProgress"

        def get_job_type(val):
            if val == 0:
                return "Competitor Scraping Job"
            elif val == 1:
                return "New Products"
            return "Product Competitors"

        def get_competitors_info(val):
            if val == 0:
                return 'All Competitors'
            else:
                return ProductCompetitorSites.objects.get(reference_id=val).name

        def get_category_info(val):
            if val == 0:
                return 'All Categories'
            else:
                return Categories.objects.get(id=val).name

        def get_supplier_info(val):
            if val == 0:
                return 'All Suppliers'
            else:
                return Suppliers.objects.get(id=val).name

        def extract(obj, key):
            dict_main = {'sr_no': key, 'created_at': str(obj.created_at),
                         'competitors': get_competitors_info(obj.competitor),
                         'products': obj.product_list,
                         'job_type': get_job_type(obj.job_type),
                         'job_status': get_job_status(obj.status),
                         'price_changes': obj.products_price_changes,
                         'category': get_category_info(obj.category),
                         'supplier': get_supplier_info(obj.supplier),
                         'job_progress': obj.status_of_job}
            return dict_main

        items = paginate(job_logs_, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)

    _suppliers = Suppliers.objects.all()
    _categories = Categories.objects.all()
    return render(request, 'products/instant_push.html', context={'suppliers': _suppliers,
                                                                  'categories': _categories})


@login_required
def register_push_event(request):
    if request.method == 'POST':
        products_ = request.POST['product']
        competitor = request.POST['competitor']
        supplier_ = request.POST['supplier']
        category = request.POST['category']

        ijd = InstantJobDeclaration.objects.create(competitor=competitor, product_list=products_,
                                                   supplier=supplier_, category=category, job_type=0)

        # products = Products.objects.all()
        # if ijd.competitor != 0 and ijd.competitor != '0':
        #     products = products.filter(productcompetitorslinks__site_reference__reference_id=ijd.competitor)
        # if ijd.supplier != 0 and ijd.competitor != '0':
        #     products = products.filter(supplier__id=ijd.supplier)
        # if ijd.category != 0 and ijd.competitor != '0':
        #     products = products.filter(categories__id=ijd.category)
        # if ijd.product_list != '':
        #     product_list = ijd.product_list.split(',')
        #     products = products.filter(sku__in=product_list)
        #
        # print(len(products))
        from .tasks import start_product_competitor_job
        start_product_competitor_job(ijd.id)

        return redirect('/app/instant_push')


@login_required
def register_products_job(request):
    from .tasks import start_product_and_other_detail_fetching
    ijd = InstantJobDeclaration.objects.create(job_type=1)
    start_product_and_other_detail_fetching(ijd.id)
    return redirect('/app/instant_push')


@login_required
def register_product_competitor_job(request):
    from .tasks import start_product_competitor_fetching
    ijd = InstantJobDeclaration.objects.create(job_type=2)
    start_product_competitor_fetching(ijd.id)
    return redirect('/app/instant_push')


@login_required
def competitors_info(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 10
        filter_type = int(data['filter_type'])
        filter_type2 = int(data['filter_type2'])
        product_sku = data['product_sku']

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
                Q(product__name__icontains=product_sku) | Q(product__sku__icontains=product_sku))

        def get_date_time_from_datetime(obj):
            return datetime.datetime.strftime(obj, '%d-%m-%Y %H:%M')

        def get_date_from_datetime(obj):
            return datetime.datetime.strftime(obj, '%d-%m-%Y')

        def extract(obj, key):
            competitor_link_list = []
            categories_ = [x.name for x in obj.product.categories.all()]
            categories_ = ','.join(categories_)

            expected_price = obj.expected_price
            if obj.expected_price == 0 or obj.expected_price == 0.0:
                expected_price = 'N/A'

            is_smart_price_set_applied = 'No'
            if obj.is_smart_price_set_applied:
                is_smart_price_set_applied = 'Yes'

            dict_main = {'sr_no': key, 'sku': obj.product.sku, 'name': obj.product.name, 'categories': categories_,
                         'competitor_name': 'Thenx', 'price': obj.product_price, 'cost': obj.product_cost,
                         'margin': '-',
                         'stock': '-',
                         'all_cost_price': obj.all_cost_price,
                         'id': obj.id,
                         'is_smart_price_set_applied': is_smart_price_set_applied,
                         'link_status': 'Active', 'last_price_date': '-', 'price_diff': '-',
                         'last_check': get_date_time_from_datetime(obj.product.updated_at),
                         'smart_price': expected_price,
                         'link': obj.product.url}
            competitor_link_list.append(dict_main)

            for obj2 in obj.competitor_site_log.all():
                status__, last_time_date, last_time = 'Active', '-', '-'
                if obj2.is_error:
                    status__ = 'InActive'

                if obj2.competitor_link:
                    last_time_update = ProductCompetitorSitesReference.objects.filter(
                        competitor_link=obj2.competitor_link).order_by('-id')
                    if last_time_update.count() > 2:
                        last_time_update = last_time_update[1]
                        last_time_date = str(last_time_update.promotion_price) + '/' + get_date_from_datetime(
                            last_time_update.created_at)
                        last_time = get_date_time_from_datetime(last_time_update.created_at)

                if obj2.is_error:
                    promotion_price = 'N/A'
                    product_cost = 'N/A'
                    price_diff = 'N/A'
                    stock = 'N/A'

                else:
                    promotion_price = 0.0
                    if obj2.promotion_price:
                        promotion_price = float(obj2.promotion_price)
                    product_cost = obj.product_cost
                    stock = obj2.stock_entry
                    price_diff = round(promotion_price - obj.product_price)

                site_reference_name = ''
                if obj2.site_reference:
                    site_reference_name = obj2.site_reference.name

                dict_inner = {'sr_no': '', 'sku': '', 'name': '', 'categories': '',
                              'competitor_name': site_reference_name, 'price': promotion_price,
                              'cost': product_cost, 'all_cost_price': '',
                              'margin': '-', 'stock': stock,
                              'is_smart_price_set_applied': '',
                              'link_status': status__, 'last_price_date': last_time_date,
                              'price_diff': price_diff,
                              'last_check': last_time,
                              'smart_price': '',
                              'link': obj2.link}
                competitor_link_list.append(dict_inner)
            competitor_link_list.append({'sr_no': '', 'sku': '', 'name': '', 'categories': '',
                                         'competitor_name': '', 'price': '',
                                         'cost': '',
                                         'all_cost_price': '',
                                         'margin': '', 'stock': '',
                                         'is_smart_price_set_applied': '',
                                         'link_status': '', 'last_price_date': '',
                                         'price_diff': '',
                                         'smart_price': '',
                                         'last_check': '',
                                         'link': ''})
            return competitor_link_list

        items = paginate(_admin_logs, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/competitors_info.html', context={})


@login_required
def suppliers(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        _suppliers = Suppliers.objects.all().order_by('id')
        if search_parameter:
            _suppliers = Suppliers.objects.filter(name__icontains=search_parameter).order_by('id')

        def extract(obj, key):
            return {
                'sr_no': key,
                'name': obj.name,
                'reference_id': obj.reference_id,
                'total_products': Products.objects.filter(supplier=obj).count()
            }

        items = paginate(_suppliers, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/suppliers.html', context={})


def dump_categories_job(request):
    data = get_categories_list_new()

    category_id = [int(x['id']) for x in data]
    existing_categories = Categories.objects.filter(id__in=category_id).values_list('id', flat=True)
    category_to_create = list(set(category_id) - set(existing_categories))
    category_to_create = list(filter(lambda x: int(x['id']) in category_to_create, data))
    category_to_create = list({x['id']: x for x in category_to_create}.values())
    Categories.objects.bulk_create(
        [Categories(id=x['id'], reference_id=x['id'], name=x['name'],
                    products_count=x['products_count']) for x in category_to_create])

    return redirect('products:home')


def dump_brands_job(request):
    data = get_brands_information()

    brand_ids = [int(x['id']) for x in data]
    existing_brands = Brands.objects.filter(id__in=brand_ids).values_list('id', flat=True)
    brands_to_create = list(set(brand_ids) - set(existing_brands))
    brands_to_create = list(filter(lambda x: int(x['id']) in brands_to_create, data))
    brands_to_create = list({x['id']: x for x in brands_to_create}.values())
    Brands.objects.bulk_create([Brands(id=x['id'], reference_id=x['id'], name=x['name']) for x in brands_to_create])
    return redirect('products:home')


def dump_suppliers_job(request):
    data = get_suppliers_information()

    supplier_ids = [int(x['id']) for x in data]
    existing_suppliers = Suppliers.objects.filter(id__in=supplier_ids).values_list('id', flat=True)
    supplier_to_create = list(set(supplier_ids) - set(existing_suppliers))
    supplier_to_create = list(filter(lambda x: int(x['id']) in supplier_to_create, data))
    supplier_to_create = list({x['id']: x for x in supplier_to_create}.values())
    Suppliers.objects.bulk_create(
        [Suppliers(id=x['id'], reference_id=x['id'], name=x['name']) for x in supplier_to_create])

    return redirect('products:home')


def dump_competitors_info_job(request):
    cron_ = CronJobLogRunning.objects.create(cron_job_type=2)
    response_list = get_competitor_links_from_server()
    new_pro = upload_competitor_info_against_product(response_list)

    cron_.scanned_sku = len(response_list)
    cron_.new_sku = new_pro
    cron_.changed_prices = 0
    cron_.save()
    return redirect('products:home')


def dump_products_info(request):
    data = get_products_list()
    products_list_info = []
    data, brands_id, supplier_ids_list, categories_id = data

    # categories_id = list({d['id']: d for d in categories_id}.values())

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

    product_category_list = []
    for obj in products_to_create:
        if obj['brand_id'] and obj['supplier_id']:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'],
                         quantity=obj['quantity'],
                         cost=float(obj['cost']),
                         price=float(obj['price']), brand_id=int(obj['brand_id']),
                         supplier_id=int(obj['supplier_id'])))
        elif obj['brand_id']:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'], cost=float(obj['cost']),
                         quantity=obj['quantity'],
                         price=float(obj['price']), brand_id=int(obj['brand_id'])))
        elif obj['supplier_id']:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'], cost=float(obj['cost']),
                         quantity=obj['quantity'],
                         price=float(obj['price']), supplier_id=int(obj['supplier_id'])))
        else:
            products_list_info.append(
                Products(id=obj['id'], sku=obj['sku'], reference_id=int(obj['reference_id']), name=obj['name'],
                         url=obj['url'], cost=float(obj['cost']),
                         quantity=obj['quantity'],
                         price=float(obj['price'])))

        [product_category_list.append(
            Products.categories.through(categories_id=int(cat['category_id']), products_id=int(obj['id']))) for cat in
            obj['categories']]

    Products.objects.bulk_create(products_list_info)
    Products.categories.through.objects.bulk_create(product_category_list)

    return redirect('products:home')


@login_required
def add_rules(request):
    # Rules.objects.all().delete()
    # WarrantyRule.objects.all().delete()
    # MarginRules.objects.all().delete()
    # ThenxCostSupplier.objects.all().delete()
    # LocalCostSupplier.objects.all().delete()
    # PriceCompetitorRule.objects.all().delete()
    if request.method == 'POST':
        data = request.POST
        rule_type = int(data['rule_type']) if 'rule_type' in data else 0

        if rule_type == 1:
            Rule(request).add_warranty_rule()

        elif rule_type == 2:
            vat_price = data['vat_price'] if 'vat_price' in data else 0
            rule_, created = Rules.objects.get_or_create(rule_type=2)
            vat_, created = VatRule.objects.get_or_create(rule=rule_)
            vat_.percentage = vat_price
            vat_.save()

        elif rule_type == 3:
            Rule(request).add_margin_rule()

        elif rule_type == 4:
            Rule(request).add_local_cost_supplier_rule()

        elif rule_type == 5:
            Rule(request).add_thenx_cost_supplier_rule()

        elif rule_type == 6:
            Rule(request).add_price_competitor_rule()

        return redirect('/app/rules')

    _suppliers = Suppliers.objects.all()
    _categories = Categories.objects.all()
    _competitors = ProductCompetitorSites.objects.all()

    return render(request, 'products/rules_calculation/rules.html',
                  context={'suppliers': _suppliers, 'categories': _categories,
                           'competitors': _competitors})


@login_required
def add_rules_csv(request):
    rule_type = request.GET.get('rule_type')
    rule_type = int(rule_type)

    if rule_type == 3:
        AddCSVRule(request).dump_margin_rule()

    if rule_type == 1:
        AddCSVRule(request).dump_local_cost_rule()

    if rule_type == 2:
        AddCSVRule(request).dump_thenx_cost_rule()

    return redirect('/app/rules')


@login_required
def edit_rule(request):
    data = request.POST
    rule_identity = int(data['rule_identity']) if 'rule_identity' in data else 0
    rule_ = Rules.objects.get(id=rule_identity)

    rule_type = rule_.rule_type

    if rule_type == 1:
        EditRule(request, rule_).add_warranty_rule()

    elif rule_type == 3:
        EditRule(request, rule_).add_margin_rule()

    elif rule_type == 4:
        EditRule(request, rule_).add_local_cost_supplier_rule()

    elif rule_type == 5:
        EditRule(request, rule_).add_thenx_cost_supplier_rule()

    elif rule_type == 6:
        EditRule(request, rule_).add_price_competitor_rule()

    return JsonResponse(data={'success': True}, safe=False)


@login_required
def get_rule_detail(request):
    rule_id = int(request.GET.get('rule_id'))
    rule_ = Rules.objects.get(id=rule_id)
    if rule_.rule_type == 4:
        rule_ = get_local_cost_supplier(rule_)
    elif rule_.rule_type == 5:
        rule_ = get_thenx_cost_supplier(rule_)
    elif rule_.rule_type == 1:
        rule_ = get_warranty_obj(rule_)
    elif rule_.rule_type == 3:
        rule_ = get_margin_rule(rule_)
    elif rule_.rule_type == 6:
        rule_ = get_competitor_rule(rule_)
    return JsonResponse(data=rule_, safe=False)


@login_required
def rules(request):
    lcs_ = Rules.objects.filter(rule_type=4)
    lcs = []
    for obj in lcs_:
        response_ = get_local_cost_supplier(obj)
        if response_:
            lcs.append(response_)

    tcs_ = Rules.objects.filter(rule_type=5)
    tcs = []
    for obj in tcs_:
        response_ = get_thenx_cost_supplier(obj)
        if response_:
            tcs.append(response_)

    vat = Rules.objects.filter(rule_type=2).last()
    if vat:
        vat = VatRule.objects.filter(rule=vat).last().percentage

    warranty_rules_ = Rules.objects.filter(rule_type=1)
    warranty_rules = []
    for obj in warranty_rules_:
        response_ = get_warranty_obj(obj)
        if response_:
            warranty_rules.append(response_)

    margin_rules_ = Rules.objects.filter(rule_type=3)
    margin_rules = []
    for obj in margin_rules_:
        response_ = get_margin_rule(obj)
        if response_:
            margin_rules.append(response_)

    competitor_rules_ = Rules.objects.filter(rule_type=6)
    competitor_rules = []
    for obj in competitor_rules_:
        response_ = get_competitor_rule(obj)
        if response_:
            competitor_rules.append(response_)

    _suppliers = Suppliers.objects.all()
    _categories = Categories.objects.all()
    _competitors = ProductCompetitorSites.objects.all()

    return render(request, 'products/rules_viewer/rules_viewer.html',
                  context={'lcp_info': lcs, 'tcp_info': tcs, 'vat': vat,
                           'warranty_rules': warranty_rules,
                           'margin_rules': margin_rules,
                           'suppliers': _suppliers,
                           'categories': _categories,
                           'competitors_sites': _competitors,
                           'competitors': competitor_rules
                           })


@login_required
def delete_rule(request):
    id_ = request.POST.get('id', 0)
    Rules.objects.filter(id=int(id_)).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_all_rule(request):
    rule_type = request.POST.get('rule_type', 0)
    Rules.objects.filter(rule_type=int(rule_type)).delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def filter_costs_viewer(request):
    response_ = RulesFilter(request).get_response()
    return JsonResponse(data=response_, safe=False)


@login_required
def filter_margin_rules(request):
    response_ = RulesFilter(request).get_response()
    return JsonResponse(data=response_, safe=False)


def products_sku(request):
    search = request.GET.get('q', '')
    pro_ = Products.objects.filter(sku__istartswith=search)
    pro_ = [x.sku for x in pro_]
    return JsonResponse(data=pro_, safe=False)


def test_product_cron(request):
    from .product_competitor_fetching import product_competitor_fetching_jobs
    try:
        product_competitor_fetching_jobs()
    except Exception as e:
        print(e)
    return JsonResponse(data={'hello': 'hello'}, safe=False)


def test_product_competitor_link(request):
    from .product_competitor_links_from_server import product_competitor_fetching_job_from_server
    try:
        product_competitor_fetching_job_from_server()
    except Exception as e:
        print(e)
    return JsonResponse(data={'hello': 'hello'}, safe=False)


def test_product_scrapping(request):
    from .product_competitor_fetching import product_competitor_fetching_jobs
    try:
        product_competitor_fetching_jobs()
    except Exception as e:
        print(e)
    return JsonResponse(data={'hello': 'hello'}, safe=False)


def test_product_fetching_items(request):
    from .product_fetching_job import product_fetching_jobs
    product_fetching_jobs()
    return JsonResponse(data={'hello': 'hello'}, safe=False)


def test_email_csv_files(request):
    filename = "cron_logs" + str(datetime.datetime.now().timestamp()) + '.csv'
    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), filename)

    cron_job_logs(filename)

    filename2 = "competitor_logs" + str(datetime.datetime.now().timestamp()) + '.csv'
    filename2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), filename2)
    competitor_information_logs(filename2)

    send_email_user('Cron Logs', 'products/email_templates/daily_update_mail.html', attach_file=[filename, filename2])

    try:
        os.remove(filename)
        os.remove(filename2)
    except Exception as e:
        print(e)

    return JsonResponse(data={'hello': 'hello'}, safe=False)


@login_required
def upload_products(request):
    error_ = ""
    is_csv_file = True
    if request.method == "POST":
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            error_ = "This is not a csv file"
            is_csv_file = False

        if is_csv_file:
            try:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=','):
                    try:
                        # Products.objects.update_or_create(sku=column[0].strip(),
                        #                               defaults={"name": column[2], "smart_price_value": column[3],
                        #                                         "is_smart_price_already_set": True})
                        Products.objects.update_or_create(id=int(column[0]), reference_id=int(column[0]),
                                                          sku=column[1].strip(),
                                                          defaults={"name": column[4], "price": column[2],
                                                                    "cost": column[3]})
                    except Exception as e:
                        print (e)
            except Exception as e:
                print(e)
    return render(request, 'products/upload_products.html', context={'error': error_})


@login_required
def upload_product_competitors(request):
    error_ = ""
    is_csv_file = True
    if request.method == "POST":
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            error_ = "This is not a csv file"
            is_csv_file = False

        if is_csv_file:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            for column in csv.reader(io_string, delimiter=','):
                try:
                    prod_ = Products.objects.get(sku=column[0].strip())
                    competitor_id = ProductCompetitorSites.objects.filter(name__iexact=column[1]).last()
                    ProductCompetitorsLinks.objects.get_or_create(product=prod_, site_reference=competitor_id,
                                                                  link=column[2])
                except Exception as e:
                    pass
    return render(request, 'products/upload_products.html', context={'error': error_})


@login_required
def job_logs(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        _cron_logs = CronJobLogRunning.objects.all().order_by('-id')

        def extract(obj, key):
            return {
                'sr_no': key,
                'job_name': get_job_type(obj.cron_job_type),
                'started_at': datetime.datetime.strftime(obj.created_at, '%Y-%m-%d %I:%M %p'),
                'action': get_job_action(obj.cron_job_type),
                'scanned_sku': get_new_products_count(obj.scanned_sku),
                'changed_prices': get_new_products_count(obj.changed_prices),
                'new_sku': get_new_products_count(obj.new_sku),
                'report': 'Report'
            }

        items = paginate(_cron_logs, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/cron_job_logs.html', context={})


@login_required
def job_detail(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0
        search_parameter = data['search[value]'] if 'search[value]' in data else ''

        _admin_logs = AdminLogOfJobToShow.objects.all().order_by('-id')
        if search_parameter:
            _admin_logs = AdminLogOfJobToShow.objects.filter(product__sku__icontains=search_parameter).order_by('id')

        def extract(obj, key):
            return {
                'sr_no': key,
                'product': obj.product.sku,
                'created_at': datetime.datetime.strftime(obj.created_at, '%Y-%m-%d %I:%M %p'),
                'total_competitors_link': obj.total_competitors_link,
                'cheapest_price': obj.cheapest_price,
                'highest_price': obj.highest_price,
                'is_approved': obj.is_approved,
                'is_valid': obj.is_valid
            }

        items = paginate(_admin_logs, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)
    return render(request, 'products/job_details.html', context={})


def custom_404_page(request, exception):
    return render(request, "products/404.html", {}, status=404)


def custom_500_page(request, exception=None):
    return render(request, 'products/500.html', status=500)


def delete_all_data(request):
    ProductCompetitorSitesReference.objects.all().delete()
    Categories.objects.all().delete()
    Brands.objects.all().delete()
    Suppliers.objects.all().delete()
    Products.objects.all().delete()
    ProductCalculationInformation.objects.all().delete()
    ProductCalculationInformationFormulas.objects.all().delete()
    ProductCompetitorsLinks.objects.all().delete()
    SupplierDetailPrices.objects.all().delete()
    Rules.objects.all().delete()
    WarrantyRule.objects.all().delete()
    VatRule.objects.all().delete()
    MarginRules.objects.all().delete()
    LocalCostSupplier.objects.all().delete()
    ThenxCostSupplier.objects.all().delete()
    PriceCompetitorRule.objects.all().delete()
    CronJobLogRunning.objects.all().delete()
    LogErrorWhileScraping.objects.all().delete()
    AdminLogOfJobToShow.objects.all().delete()
    return JsonResponse(data={'success': True}, safe=False)


def delete_competitors_data(request):
    ProductCompetitorSitesReference.objects.all().delete()
    LogErrorWhileScraping.objects.all().delete()
    AdminLogOfJobToShow.objects.all().delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def reset_password(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    password = data['password']
    up = UsersPermissions.objects.get(id=int(id_))
    user = up.user
    user.set_password(password)
    user.save()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def delete_user(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    up = UsersPermissions.objects.get(id=int(id_))
    if not up.user.is_superuser:
        user = up.user
        user.delete()
        up.delete()
    return JsonResponse(data={'success': True}, safe=False)


@login_required
def update_permission_of_user(request):
    data = json.loads(request.body.decode('utf-8'))
    id_ = data['id']
    is_home_page = data['is_home_page']
    is_products_page = data['is_products_page']
    is_competitors_page = data['is_competitors_page']
    is_daily_price_page = data['is_daily_price_page']
    is_active_links_page = data['is_active_links_page']
    is_cron_job_logs_page = data['is_cron_job_logs_page']
    up = UsersPermissions.objects.get(id=int(id_))
    up.is_home_page = is_home_page
    up.is_products_page = is_products_page
    up.is_competitors_page = is_competitors_page
    up.is_daily_price_page = is_daily_price_page
    up.is_active_links_page = is_active_links_page
    up.is_cron_job_logs_page = is_cron_job_logs_page
    up.save()

    permissions_ = []
    if up.is_home_page:
        permissions_.append('home_page')
    if up.is_products_page:
        permissions_.append('products_page')
    if up.is_competitors_page:
        permissions_.append('competitors_info')
    if up.is_daily_price_page:
        permissions_.append('daily_changes')
    if up.is_active_links_page:
        permissions_.append('active_changes')
    if up.is_cron_job_logs_page:
        permissions_.append('cron_job_logs')
    permissions_ = ','.join(permissions_)
    return JsonResponse(data={'success': True, 'permissions': permissions_}, safe=False)


from django.contrib import messages


@login_required
def add_new_user(request):
    data = request.POST
    is_home_page = data['is_home_page'] if 'is_home_page' in data else False
    is_products_page = data['is_products_page'] if 'is_products_page' in data else False
    is_competitors_page = data['is_competitors_page'] if 'is_competitors_page' in data else False
    is_daily_price_page = data['is_daily_price_page'] if 'is_daily_price_page' in data else False
    is_active_links_page = data['is_active_links_page'] if 'is_active_links_page' in data else False
    is_cron_job_logs_page = data['is_cron_job_logs_page'] if 'is_cron_job_logs_page' in data else False
    name = data['name']
    email_address = data['email_address']
    password = data['password']

    if is_home_page:
        is_home_page = True
    if is_products_page:
        is_products_page = True
    if is_competitors_page:
        is_competitors_page = True
    if is_daily_price_page:
        is_daily_price_page = True
    if is_active_links_page:
        is_active_links_page = True
    if is_cron_job_logs_page:
        is_cron_job_logs_page = True

    email_address = email_address.lower().strip()

    user, created = User.objects.get_or_create(username=email_address, email=email_address)
    if not created:
        messages.error(request, 'This email address already exists')
        return redirect('products:users_info')

    user.set_password(password)
    user.first_name = name
    user.save()

    up, created = UsersPermissions.objects.get_or_create(user=user)
    up.is_home_page = is_home_page
    up.is_products_page = is_products_page
    up.is_competitors_page = is_competitors_page
    up.is_daily_price_page = is_daily_price_page
    up.is_active_links_page = is_active_links_page
    up.is_cron_job_logs_page = is_cron_job_logs_page
    up.save()

    return redirect('products:users_info')


@login_required
def users_info(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 0

        _users = UsersPermissions.objects.filter(user__is_superuser=False).order_by('-id')

        def extract(obj, key):
            permissions_ = []
            if obj.is_home_page:
                permissions_.append('home_page')
            if obj.is_products_page:
                permissions_.append('products_page')
            if obj.is_competitors_page:
                permissions_.append('competitors_info')
            if obj.is_daily_price_page:
                permissions_.append('daily_changes')
            if obj.is_active_links_page:
                permissions_.append('active_changes')
            if obj.is_cron_job_logs_page:
                permissions_.append('cron_job_logs')
            permissions_ = ','.join(permissions_)
            return {
                'sr_no': key,
                'id': obj.id,
                'name': obj.user.first_name,
                'email': obj.user.username,
                'permissions': permissions_,
                'is_home_page': obj.is_home_page,
                'is_products_page': obj.is_products_page,
                'is_competitors_page': obj.is_competitors_page,
                'is_daily_price_page': obj.is_daily_price_page,
                'is_active_links_page': obj.is_active_links_page,
                'is_cron_job_logs_page': obj.is_cron_job_logs_page
            }

        items = paginate(_users, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)

    return render(request, 'products/users.html', context={})


@login_required
def download_csv_file(request):
    rule_type = request.GET.get('rule_type')
    rule_type = int(rule_type)

    directory_path = os.path.join('products', 'templates', 'products', 'sample_csv_files')
    file_path = os.path.join(settings.BASE_DIR, directory_path)

    if rule_type == 3:
        file_path = os.path.join(file_path, 'margin_rule.csv')
    elif rule_type == 1:
        file_path = os.path.join(file_path, 'localcostrule.csv')
    elif rule_type == 2:
        file_path = os.path.join(file_path, 'thenxcostrule.csv')
    elif rule_type == 4:
        file_path = os.path.join(file_path, 'localcostrule.csv')

    data = open(file_path, 'r').read()
    resp = HttpResponse(data, content_type='application/x-download')
    resp['Content-Disposition'] = 'attachment;filename=rule_definition.csv'
    return resp


@login_required
def export_csv_file(request):
    rule_type = request.GET.get('rule_type')
    rule_type = int(rule_type)

    export_rule_to_file(rule_type)

    directory_path = os.path.join('products', 'templates', 'products', 'export_rules')
    file_path = os.path.join(settings.BASE_DIR, directory_path)

    if rule_type == 3:
        file_path = os.path.join(file_path, 'export_margin_rule.csv')
    elif rule_type == 4:
        file_path = os.path.join(file_path, 'export_local_cost.csv')
    elif rule_type == 5:
        file_path = os.path.join(file_path, 'export_thenx_cost.csv')

    data = open(file_path, 'r').read()
    resp = HttpResponse(data, content_type='application/x-download')
    resp['Content-Disposition'] = 'attachment;filename=export_rule.csv'
    return resp


@login_required
def export_products_csv_file(request):
    export_product_to_file()
    directory_path = os.path.join('products', 'templates', 'products', 'export_pages', 'products.csv')
    file_path = os.path.join(settings.BASE_DIR, directory_path)
    data = open(file_path, 'r').read()
    resp = HttpResponse(data, content_type='application/x-download')
    resp['Content-Disposition'] = 'attachment;filename=export_products.csv'
    return resp


@login_required
def export_scraping_csv_file(request):
    export_scraping_to_file()
    directory_path = os.path.join('products', 'templates', 'products', 'export_pages', 'competitors.csv')
    file_path = os.path.join(settings.BASE_DIR, directory_path)
    data = open(file_path, 'r').read()
    resp = HttpResponse(data, content_type='application/x-download')
    resp['Content-Disposition'] = 'attachment;filename=export_scraping.csv'
    return resp
