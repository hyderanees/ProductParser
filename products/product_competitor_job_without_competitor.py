from statistics import mean

from products.models import *
import datetime
from .utils import calculate_price_detail_of_product


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


def product_competitor_job_without_competitor():
    cron_ = CronJobLogRunning.objects.create(cron_job_type=4)
    products = ProductCompetitorsLinks.objects.all().values('product__id').distinct()
    products = Products.objects.all().exclude(id__in=products)

    scanned_sku = 0
    price_changes_count = 0

    for prod in products:
        pcsr_list = []
        is_price_change = False
        scanned_sku = scanned_sku + 1

        expected_price = 0
        original_price_applied = True
        margin_rule_applied = False
        competitor_rule_applied = False
        # response__ = calculate_price_detail_of_product(prod)
        all_cost_price = prod.all_cost_price

        if expected_price == 0 or expected_price == 0.0:
            retail_sale_price = prod.retail_price
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

        alojts = AdminLogOfJobToShow.objects.create(product=prod, total_competitors_link=0,
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

        cron_.scanned_sku = scanned_sku
        cron_.changed_prices = price_changes_count
        cron_.save()

