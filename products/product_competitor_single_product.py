from statistics import mean

from products.models import *
from sitesparser.distrizone import DistriZoneInformation
from sitesparser.gsmnet import GSMNETInformation
from sitesparser.inowgsm import InowGSMInformation
from sitesparser.magazingsm import MagaZingSMInformation
from sitesparser.moka_gsm import MokaGSMInformation
from sitesparser.powerlaptop import PowerLaptopInformation
from sitesparser.protableta import ProtabletaInformation
from sitesparser.servicepack import ServicePackInformation
from sitesparser.sepmobile import SEPMobileMainFunction
from sitesparser.sunnex import SunnexMobile
from sitesparser.tradegsm import TradeGSMInformation

from .utils import calculate_price_detail_of_product


class FetchProductDetail:

    def __init__(self, obj):
        self.product_competitor = obj
        self.response_param = False

    def iterate_over_obj(self):
        if self.product_competitor.site_reference.reference_id == 1:
            return self.get_detail_of_distrizone(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 2:
            return self.get_detail_of_gsmnet(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 3:
            return self.get_detail_of_inowgsm(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 4:
            return self.get_detail_of_magazingsm(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 5:
            return self.get_detail_of_mokagsm(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 6:
            return self.get_detail_of_powerlaptop(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 7:
            return self.get_detail_of_protableta(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 8:
            return self.get_detail_of_servicepack(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 9:
            return self.get_detail_of_sepmobile(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 10:
            return self.get_detail_of_sunnex_mobile(self.product_competitor.link)
        if self.product_competitor.site_reference.reference_id == 12:
            return self.get_detail_of_tradegsm_mobile(self.product_competitor.link)

    def get_detail_of_distrizone(self, url):
        try:
            self.response_param = DistriZoneInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='Distrizone', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_gsmnet(self, url):
        try:
            self.response_param = GSMNETInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='GSMNETInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_inowgsm(self, url):
        try:
            self.response_param = InowGSMInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='InowGSMInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_magazingsm(self, url):
        try:
            self.response_param = MagaZingSMInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='MagaZingSMInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_mokagsm(self, url):
        try:
            self.response_param = MokaGSMInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='MokaGSMInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_powerlaptop(self, url):
        try:
            self.response_param = PowerLaptopInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='PowerLaptopInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_protableta(self, url):
        try:
            self.response_param = ProtabletaInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='ProtabletaInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_servicepack(self, url):
        try:
            self.response_param = ServicePackInformation(url).get_prices()
        except Exception as e:
            LogErrorWhileScraping.objects.create(site_name='ServicePackInformation', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_sepmobile(self, url):
        try:
            self.response_param = SEPMobileMainFunction(url)
        except Exception as e:
            print (e)
            LogErrorWhileScraping.objects.create(site_name='SepMobile', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_sunnex_mobile(self, url):
        try:
            self.response_param = SunnexMobile(url)
        except Exception as e:
            print (e)
            LogErrorWhileScraping.objects.create(site_name='SunnexMobile', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False

    def get_detail_of_tradegsm_mobile(self, url):
        try:
            self.response_param = TradeGSMInformation(url).get_prices()
        except Exception as e:
            print(e)
            LogErrorWhileScraping.objects.create(site_name='TradeGSM', link=url,
                                                 site_reference=self.product_competitor.site_reference, exception=e)
            self.response_param = False


def get_competitor_rule(product):
    filtered_ = None
    if Rules.objects.filter(rule_type=6):
        categories__ = product.categories.all()

        filtered_ = PriceCompetitorRule.objects.filter(is_on_category=False, product_sku=product).last()
        if not filtered_:
            filtered_ = PriceCompetitorRule.objects.filter(is_on_category=True, supplier=product.supplier,
                                                         is_all_categories=False,
                                                         category__in=categories__)

            if not filtered_:
                filtered_ = PriceCompetitorRule.objects.filter(is_on_category=True, supplier=product.supplier,
                                                             is_all_categories=True)
            if filtered_:
                competitors_ = ProductCompetitorSitesReference.objects.filter(product=product)
                competitors_ = [x.site_reference for x in competitors_]

                competitor_check = filtered_.filter(is_all_competitors=False, competitor__in=competitors_)
                new_competitors_rules = competitor_check
                filtered_ = list(new_competitors_rules) + list(filtered_.filter(is_all_competitors=True))

    return filtered_


def evaluate_competitor_rule(rule_, prod, new_price_list, pcsr_list):
    if rule_:

        competitor_check_list = []
        if rule_.is_all_competitors:
            competitor_check_list = new_price_list[:]
        else:
            for obj in pcsr_list:
                if obj['obj'].site_reference == rule_.competitor:
                    competitor_check_list.append(obj['price'])

        if rule_.competitor_priority == 2:
            competitor_price_ = mean(competitor_check_list)
        elif rule_.competitor_priority == 1:
            competitor_price_ = max(competitor_check_list)
        else:
            competitor_price_ = min(competitor_check_list)

        if rule_.check_pricer_priority == 1:
            if rule_.check_pricer_unit == 1:
                new_price_ = competitor_price_ + rule_.check_pricer
            else:
                percentage_amount = (competitor_price_ * (rule_.check_pricer / 100))
                new_price_ = competitor_price_ + percentage_amount
        else:
            if rule_.check_pricer_unit == 1:
                new_price_ = competitor_price_ - rule_.check_pricer
            else:
                percentage_amount = (competitor_price_ * (rule_.check_pricer / 100))
                new_price_ = competitor_price_ - percentage_amount

        if rule_.final_price_unit == 2:
            check_price = (prod.cost * (rule_.final_price_check / 100))
            check_price_ = prod.cost + check_price
        else:
            check_price_ = prod.cost + rule_.final_price_check

        print ('new_price', new_price_, 'check_price', check_price_)
        if new_price_ > check_price_:
            new_price_ = round(new_price_, 2)
            return new_price_
        else:
            return 0

    return 0


def single_product_scrapping_test_job(sku):
    products = Products.objects.filter(sku__iexact=sku.strip())

    scanned_sku = 0
    price_changes_count = 0

    for prod in products:
        pcl = ProductCompetitorsLinks.objects.filter(product=prod)
        pcsr_list = []
        is_price_change = False
        scanned_sku = scanned_sku + 1

        for obj in pcl:
            response_ = FetchProductDetail(obj)
            response_.iterate_over_obj()
            response_ = response_.response_param
            old_price = 'N/A'

            if response_:
                pcsr = ProductCompetitorSitesReference.objects.filter(product=obj.product,
                                                                      competitor_link=obj,
                                                                      link=obj.link).last()
                if pcsr:
                    if pcsr.promotion_price != str(response_['promotion_price']):
                        is_price_change = True
                    old_price = pcsr.promotion_price
                else:
                    is_price_change = True

                pcsr = ProductCompetitorSitesReference.objects.create(product=obj.product,
                                                                      competitor_link=obj,
                                                                      link=obj.link,
                                                                      old_price=old_price,
                                                                      site_reference=obj.site_reference,
                                                                      stock_entry=response_['stock'],
                                                                      comp_price=response_['original_price'],
                                                                      promotion_price=response_['promotion_price'],
                                                                      is_error=False)
            else:
                pcsr = ProductCompetitorSitesReference.objects.create(product=obj.product,
                                                                      competitor_link=obj,
                                                                      old_price=old_price,
                                                                      site_reference=obj.site_reference,
                                                                      link=obj.link,
                                                                      is_error=True)
            if response_:
                pcsr_list.append({'obj': pcsr, 'price': response_['promotion_price']})
            else:
                pcsr_list.append({'obj': pcsr, 'price': 0})

        if pcl:
            new_pcsr_list = [x for x in pcsr_list if x['price'] != 0]

            cheapest_price_text = min(pcsr_list, key=lambda x: x['price'])
            highest_price_text = max(pcsr_list, key=lambda x: x['price'])
            average_price_text = sum([obj['price'] for obj in pcsr_list]) / len(pcsr_list)

            cheapest_price = cheapest_price_text['price']
            highest_price = cheapest_price_text['price']

            cheapest_price_text = cheapest_price_text['obj'].site_reference.name
            highest_price_text = highest_price_text['obj'].site_reference.name

            new_price_list_ = [float(x['price']) for x in pcsr_list]
            new_price_list = [float(x['price']) for x in pcsr_list]
            new_price_list__ = [float(x['price']) for x in new_pcsr_list]

            new_price_list_.append(prod.price)
            new_price_list_ = sorted(new_price_list_)
            rank = new_price_list_.index(prod.price)
            rank = rank + 1

            if is_price_change:
                price_changes_count = price_changes_count + 1

            is_competitor_less_than_cost = False
            for obj in pcsr_list:
                if obj['price'] != 0 or obj['price'] != 0.0:
                    if obj['price'] < prod.cost:
                        is_competitor_less_than_cost = True

            expected_price = 0
            original_price_applied = True
            margin_rule_applied = False
            competitor_rule_applied = False

            response__ = calculate_price_detail_of_product(prod)
            all_cost_price = response__['all_cost_price']

            if set(new_price_list) != {0.0}:
                try:
                    rule_ = get_competitor_rule(prod)
                    for obj in rule_:
                        try:
                            # expected_price = evaluate_competitor_rule(obj, prod, new_price_list, pcsr_list)
                            expected_price = evaluate_competitor_rule(obj, prod, new_price_list__, new_pcsr_list)
                            if expected_price != 0 or expected_price != 0.0:
                                competitor_rule_applied = True
                                margin_rule_applied = False
                                original_price_applied = False
                                break
                        except Exception as e:
                            print (e)
                except Exception as e:
                    print (e)

            if expected_price == 0 or expected_price == 0.0:
                retail_sale_price = response__['retail_price_rounded']
                if retail_sale_price != 0 and retail_sale_price != 0.0 and retail_sale_price != 'N/A':
                    try:
                        expected_price = retail_sale_price
                        competitor_rule_applied = False
                        margin_rule_applied = True
                        original_price_applied = False
                    except Exception as e:
                        print (e)

            if expected_price == 0 or expected_price == 0.0 or expected_price == 'N/A':
                expected_price = prod.price
                competitor_rule_applied = False
                margin_rule_applied = False
                original_price_applied = True

            price_change_effect = 1
            price_diff = expected_price - prod.price
            if price_diff > 0:
                price_change_effect = 2
            elif price_diff < 0:
                price_change_effect = 3
            elif price_diff == 0:
                price_change_effect = 1

            same_moment_calculated_price = expected_price
            is_smart_price_set_applied = False
            if prod.is_smart_price_already_set:
                expected_price = prod.smart_price_value
                is_smart_price_set_applied = True

            AdminLogOfJobToShow.objects.filter(product=prod).update(is_valid=False)

            alojts = AdminLogOfJobToShow.objects.create(product=prod, total_competitors_link=pcl.count(),
                                                        is_valid=True, is_approved=False,
                                                        cheapest_price=float(cheapest_price),
                                                        highest_price=float(highest_price),
                                                        average_price=float(average_price_text),
                                                        cheapest_price_text=cheapest_price_text,
                                                        highest_price_text=highest_price_text,
                                                        average_price_text=average_price_text,
                                                        rank_of_product=rank,
                                                        same_moment_calculated_price=same_moment_calculated_price,
                                                        all_cost_price=all_cost_price,
                                                        is_competitor_rule_applied=competitor_rule_applied,
                                                        is_original_price_applied=original_price_applied,
                                                        is_margin_rule_applied=margin_rule_applied,
                                                        price_change_effect=price_change_effect,
                                                        product_cost=prod.cost,
                                                        product_price=prod.price,
                                                        is_competitor_asscoiated=True,
                                                        is_smart_price_set_applied=is_smart_price_set_applied,
                                                        expected_price=expected_price,
                                                        is_price_change=is_price_change,
                                                        is_competitor_less_than_cost=is_competitor_less_than_cost
                                                        )
            alojts.competitor_site_log.add(*[x['obj'] for x in pcsr_list])
        else:
            expected_price = 0
            original_price_applied = True
            margin_rule_applied = False
            competitor_rule_applied = False
            response__ = calculate_price_detail_of_product(prod)
            all_cost_price = response__['all_cost_price']

            if expected_price == 0 or expected_price == 0.0:
                retail_sale_price = response__['retail_price_rounded']
                if retail_sale_price != 0 and retail_sale_price != 0.0 and retail_sale_price != 'N/A':
                    try:
                        expected_price = retail_sale_price
                        competitor_rule_applied = False
                        margin_rule_applied = True
                        original_price_applied = False
                    except Exception as e:
                        print(e)

            if expected_price == 0 or expected_price == 0.0 or expected_price == 'N/A':
                expected_price = prod.price
                competitor_rule_applied = False
                margin_rule_applied = False
                original_price_applied = True

            price_change_effect = 1
            price_diff = expected_price - prod.price
            if price_diff > 0:
                price_change_effect = 2
            elif price_diff < 0:
                price_change_effect = 3
            elif price_diff == 0:
                price_change_effect = 0

            AdminLogOfJobToShow.objects.filter(product=prod).update(is_valid=False)

            same_moment_calculated_price = expected_price
            is_smart_price_set_applied = False
            if prod.is_smart_price_already_set:
                expected_price = prod.smart_price_value
                is_smart_price_set_applied = True

            alojts = AdminLogOfJobToShow.objects.create(product=prod, total_competitors_link=pcl.count(),
                                                        is_valid=True, is_approved=False,
                                                        cheapest_price=float(prod.price),
                                                        highest_price=float(prod.price),
                                                        average_price=float(prod.price),
                                                        cheapest_price_text=str(prod.price),
                                                        highest_price_text=str(prod.price),
                                                        average_price_text=str(prod.price),
                                                        rank_of_product=0,
                                                        all_cost_price=all_cost_price,
                                                        is_competitor_rule_applied=competitor_rule_applied,
                                                        is_original_price_applied=original_price_applied,
                                                        is_margin_rule_applied=margin_rule_applied,
                                                        price_change_effect=price_change_effect,
                                                        product_cost=prod.cost,
                                                        same_moment_calculated_price=same_moment_calculated_price,
                                                        product_price=prod.price,
                                                        is_competitor_asscoiated=False,
                                                        is_smart_price_set_applied=is_smart_price_set_applied,
                                                        expected_price=expected_price,
                                                        is_price_change=is_price_change
                                                        )
            alojts.competitor_site_log.add(*[x['obj'] for x in pcsr_list])