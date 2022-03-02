import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from newproductsiteparser.models import *
from django.shortcuts import render
from django.http import JsonResponse
from .utils import paginate


@login_required
def get_new_product_details(request):
    if request.method == 'POST':
        data = request.POST
        draw = int(data['draw']) if 'draw' in data else 0
        start_index = int(data['start']) if 'start' in data else 0
        length = int(data['length']) if 'length' in data else 10

        competitor = request.POST['competitor']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        if start_date:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date > end_date:
            start_date = None
            end_date = None

        if not start_date:
            start_date = datetime.datetime.now() - timedelta(7)
            start_date = start_date.date()
        if not end_date:
            end_date = datetime.datetime.now()

        data_1 = []
        data_2 = []
        data_3 = []
        data_4 = []
        data_5 = []
        data_6 = []
        data_7 = []
        data_8 = []

        if competitor == '0' or competitor == 0 or competitor == 3 or competitor == '3':
            data_1 = MokaGsmExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                            created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_1 = [{'competitor': 'Mokagsm', 'detail': x} for x in data_1]
        if competitor == '0' or competitor == 0 or competitor == 2 or competitor == '2':
            data_2 = PortabletaExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                               created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_2 = [{'competitor': 'Protableta', 'detail': x} for x in data_2]
        if competitor == '0' or competitor == 0 or competitor == 4 or competitor == '4':
            data_3 = MagazingGsmExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                                created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_3 = [{'competitor': 'Magazingsm', 'detail': x} for x in data_3]
        if competitor == '0' or competitor == 0 or competitor == 1 or competitor == '1':
            data_4 = ServicePackExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                                created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_4 = [{'competitor': 'Service Pack', 'detail': x} for x in data_4]
        if competitor == '0' or competitor == 0 or competitor == 5 or competitor == '5':
            data_5 = GsmnetExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                           created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_5 = [{'competitor': 'Gsmnet', 'detail': x} for x in data_5]
        if competitor == '0' or competitor == 0 or competitor == 6 or competitor == '6':
            data_6 = DistrizoneExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                               created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_6 = [{'competitor': 'Distrizone', 'detail': x} for x in data_6]
        if competitor == '0' or competitor == 0 or competitor == 7 or competitor == '7':
            data_7 = SunnexExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                           created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_7 = [{'competitor': 'Sunnex', 'detail': x} for x in data_7]
        if competitor == '0' or competitor == 0 or competitor == 8 or competitor == '8':
            data_8 = SepMobileExistingProducts.objects.filter(created_at__date__gte=start_date,
                                                              created_at__date__lte=end_date). \
                values('title', 'price', 'promotional_price', 'href_link', 'img_tag', 'created_at')
            data_8 = [{'competitor': 'SepMobile', 'detail': x} for x in data_8]

        data_ = data_1 + data_2 + data_3 + data_4 + data_5 + data_6 + data_7 + data_8

        def extract(obj, key):
            comp_ = obj['competitor']
            obj = obj['detail']
            dict_main = {'sr_no': key, 'image': obj['img_tag'], 'title': obj['title'], 'href': obj['href_link'],
                         'original_price': obj['price'], 'promotional_price': obj['promotional_price'],
                         'competitor': comp_,
                         'created_at': datetime.datetime.strftime(obj['created_at'], '%b %d, %Y')}
            return dict_main

        items = paginate(data_, extract, start_index, length, draw)
        return JsonResponse(data=items, safe=False)

    return render(request, 'products/new_product_detail_template.html', context={})
