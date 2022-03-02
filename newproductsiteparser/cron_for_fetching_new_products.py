from products.models import CronJobLogRunning, WeeklyReportNewProducts
from newproductsiteparser.models import *
from newproductsiteparser.magazingsm_new_product import MagaZingSMInformationNewProducts
from newproductsiteparser.service_pack_new_product import ServicePackInformationNewProducts
from newproductsiteparser.moka_gsm_new_product import MokaGSMInformationNewProducts
from newproductsiteparser.portableta_new_product import PortabletaInformationNewProducts
from newproductsiteparser.distrizone_new_products import DistrizoneInformationNewProducts
from newproductsiteparser.gsmnet_new_products import GsmnetInformationNewProducts
from newproductsiteparser.sunnex_new_product import SunnexInformationNewProducts
from newproductsiteparser.sep_mobile_new_product import SepMobileInformationNewProducts


def check_failure_and_give_chances(function_name):
    print('function', function_name)
    check_count = 0
    counter_1 = 0
    while check_count < 2:
        try:
            counter_1 = function_name()
            break
        except Exception as e:
            print(e)
            counter_1 = 0
        check_count = check_count + 1
    print('counter', counter_1)
    print('check count', check_count)
    return counter_1


def cron_product_fetching_competitor_new_product():
    cron_ = CronJobLogRunning.objects.create(cron_job_type=3)

    counter_1 = check_failure_and_give_chances(magazin_gsm_data)
    counter_2 = check_failure_and_give_chances(moka_gsm_data)
    counter_3 = check_failure_and_give_chances(service_pack_data)
    counter_4 = check_failure_and_give_chances(portableta_data)
    counter_5 = check_failure_and_give_chances(distrizone_data)
    counter_6 = check_failure_and_give_chances(gsmnet_data)
    counter_7 = check_failure_and_give_chances(sunnex_data)
    counter_8 = check_failure_and_give_chances(sepmobile_data)

    counter_ = counter_1 + counter_2 + counter_3 + counter_4 + counter_5 + counter_6 + counter_7 + counter_8

    WeeklyReportNewProducts.objects.create(total_new_products=counter_, service_pack_new_products=counter_3,
                                           magazingsm_new_products=counter_1, portableta_new_products=counter_4,
                                           moka_gsm_new_products=counter_2, distrizone_new_products=counter_5,
                                           gsmnet_new_products=counter_6, sunnex_new_products=counter_7,
                                           sep_mobile_new_products=counter_8)

    cron_.scanned_sku = 0
    cron_.new_sku = counter_
    cron_.changed_prices = 0
    cron_.save()


def magazin_gsm_data():
    counter_ = 0
    mgz = MagaZingSMInformationNewProducts()
    mgz.get_products_page()
    result = mgz.resultant_list

    for obj in result:
        mgz, created = MagazingGsmExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                            defaults={'title': obj['title'],
                                                                                      'price': obj['original_price'],
                                                                                      'promotional_price': obj[
                                                                                          'promotional_price'],
                                                                                      'img_tag': obj['img_tag']
                                                                                      })
        if created:
            counter_ = counter_ + 1

    return counter_


def moka_gsm_data():
    counter_ = 0
    mkg = MokaGSMInformationNewProducts()
    mkg.get_products_page()
    result = mkg.resultant_list

    for obj in result:
        moka_, created = MokaGsmExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                          defaults={'title': obj['title'],
                                                                                    'price': obj['original_price'],
                                                                                    'promotional_price': obj[
                                                                                        'promotional_price'],
                                                                                    'img_tag': obj['img_tag']
                                                                                    })

        if created:
            counter_ = counter_ + 1

    return counter_


def service_pack_data():
    counter_ = 0
    spi = ServicePackInformationNewProducts()
    spi.get_products_page()
    result = spi.resultant_list

    for obj in result:
        sp, created = ServicePackExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                           defaults={'title': obj['title'],
                                                                                     'price': obj['original_price'],
                                                                                     'promotional_price': obj[
                                                                                         'promotional_price'],
                                                                                     'img_tag': obj['img_tag']
                                                                                     })

        if created:
            counter_ = counter_ + 1

    return counter_


def portableta_data():
    counter_ = 0
    pin = PortabletaInformationNewProducts()
    pin.get_products_page()
    result = pin.resultant_list

    for obj in result:
        pin, created = PortabletaExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                           defaults={'title': obj['title'],
                                                                                     'price': obj['original_price'],
                                                                                     'promotional_price': obj[
                                                                                         'promotional_price'],
                                                                                     'img_tag': obj['img_tag']
                                                                                     })

        if created:
            counter_ = counter_ + 1

    return counter_


def distrizone_data():
    counter_ = 0
    dis_ = DistrizoneInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        pin, created = DistrizoneExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                           defaults={'title': obj['title'],
                                                                                     'price': obj['original_price'],
                                                                                     'promotional_price': obj[
                                                                                         'promotional_price'],
                                                                                     'img_tag': obj['img_tag']
                                                                                     })

        if created:
            counter_ = counter_ + 1

    return counter_


def gsmnet_data():
    counter_ = 0
    dis_ = GsmnetInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        pin, created = GsmnetExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                       defaults={'title': obj['title'],
                                                                                 'price': obj['original_price'],
                                                                                 'promotional_price': obj[
                                                                                     'promotional_price'],
                                                                                 'img_tag': obj['img_tag']
                                                                                 })

        if created:
            counter_ = counter_ + 1

    return counter_


def sunnex_data():
    counter_ = 0
    dis_ = SunnexInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        pin, created = SunnexExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                       defaults={'title': obj['title'],
                                                                                 'price': obj['original_price'],
                                                                                 'promotional_price': obj[
                                                                                     'promotional_price'],
                                                                                 'img_tag': obj['img_tag']
                                                                                 })

        if created:
            counter_ = counter_ + 1

    return counter_


def sepmobile_data():
    counter_ = 0
    dis_ = SepMobileInformationNewProducts()
    dis_.get_products_page()
    result = dis_.resultant_list

    for obj in result:
        pin, created = SepMobileExistingProducts.objects.update_or_create(href_link=obj['href_link'],
                                                                          defaults={'title': obj['title'],
                                                                                    'price': obj['original_price'],
                                                                                    'promotional_price': obj[
                                                                                        'promotional_price'],
                                                                                    'img_tag': obj['img_tag']
                                                                                    })

        if created:
            counter_ = counter_ + 1

    return counter_
