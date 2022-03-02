from django.http import HttpResponse
from newproductsiteparser.magazingsm_new_product import MagaZingSMInformationNewProducts
from newproductsiteparser.service_pack_new_product import ServicePackInformationNewProducts
from newproductsiteparser.moka_gsm_new_product import MokaGSMInformationNewProducts
from newproductsiteparser.portableta_new_product import PortabletaInformationNewProducts
from newproductsiteparser.distrizone_new_products import DistrizoneInformationNewProducts
from newproductsiteparser.gsmnet_new_products import GsmnetInformationNewProducts
from newproductsiteparser.sunnex_new_product import SunnexInformationNewProducts
from newproductsiteparser.sep_mobile_new_product import SepMobileInformationNewProducts
from newproductsiteparser.cron_for_fetching_new_products import cron_product_fetching_competitor_new_product
from .models import *


def test_magazin_gsm_information(request):
    mgz = MagaZingSMInformationNewProducts()
    mgz.get_products_page()
    result = mgz.resultant_list

    for obj in result:
        MagazingGsmExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                             defaults={'title': obj['title'],
                                                                       'price': obj['original_price'],
                                                                       'promotional_price': obj['promotional_price'],
                                                                       'img_tag': obj['img_tag']
                                                                       })

    return HttpResponse('hello')


def test_service_pack_information(request):
    spi = ServicePackInformationNewProducts()
    spi.get_products_page()
    result = spi.resultant_list

    for obj in result:
        ServicePackExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                             defaults={'title': obj['title'],
                                                                       'price': obj['original_price'],
                                                                       'promotional_price': obj['promotional_price'],
                                                                       'img_tag': obj['img_tag']
                                                                       })

    return HttpResponse('hello')


def test_moka_gsm_information(request):
    mkg = MokaGSMInformationNewProducts()
    mkg.get_products_page()
    result = mkg.resultant_list

    for obj in result:
        MokaGsmExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                         defaults={'title': obj['title'],
                                                                   'price': obj['original_price'],
                                                                   'promotional_price': obj['promotional_price'],
                                                                   'img_tag': obj['img_tag']
                                                                   })

    return HttpResponse('hello')


def test_portableta_information(request):
    pin = PortabletaInformationNewProducts()
    pin.get_products_page()
    result = pin.resultant_list

    for obj in result:
        PortabletaExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                            defaults={'title': obj['title'],
                                                                      'price': obj['original_price'],
                                                                      'promotional_price': obj['promotional_price'],
                                                                      'img_tag': obj['img_tag']
                                                                      })

    return HttpResponse('hello')


def test_distrizone_information(request):
    dis_ = DistrizoneInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        DistrizoneExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                            defaults={'title': obj['title'],
                                                                      'price': obj['original_price'],
                                                                      'promotional_price': obj['promotional_price'],
                                                                      'img_tag': obj['img_tag']
                                                                      })

    return HttpResponse('hello')


def test_sunnex_information(request):
    dis_ = SunnexInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        SunnexExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                        defaults={'title': obj['title'],
                                                                  'price': obj['original_price'],
                                                                  'promotional_price': obj['promotional_price'],
                                                                  'img_tag': obj['img_tag']
                                                                  })

    return HttpResponse('hello')


def test_gsmnet_information(request):
    dis_ = GsmnetInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        GsmnetExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                        defaults={'title': obj['title'],
                                                                  'price': obj['original_price'],
                                                                  'promotional_price': obj['promotional_price'],
                                                                  'img_tag': obj['img_tag']
                                                                  })

    return HttpResponse('hello')


def test_sepmobile_information(request):
    dis_ = SepMobileInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        SepMobileExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                           defaults={'title': obj['title'],
                                                                     'price': obj['original_price'],
                                                                     'promotional_price': obj['promotional_price'],
                                                                     'img_tag': obj['img_tag']
                                                                     })

    return HttpResponse('hello')


def test_cron_fetching_new_product(request):
    cron_product_fetching_competitor_new_product()
    return HttpResponse('hello')
