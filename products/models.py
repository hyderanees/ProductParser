from django.contrib.auth.models import User
from django.db import models

from .constants import *


class Categories(models.Model):
    name = models.TextField(default='')
    reference_id = models.IntegerField()
    products_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Brands(models.Model):
    name = models.TextField(default='')
    reference_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Suppliers(models.Model):
    name = models.TextField(default='')
    reference_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Products(models.Model):
    name = models.TextField(default='')
    sku = models.TextField(default='')
    reference_id = models.IntegerField()
    price = models.FloatField(default=0.0)
    url = models.TextField(default='')
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True)
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, null=True)
    categories = models.ManyToManyField(Categories)
    cost = models.FloatField(default=0.0)
    # 0 for usd
    cost_unit = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    # False for price not set
    # True for price is set
    is_platform_price_set = models.BooleanField(default=False)
    is_smart_price_already_set = models.BooleanField(default=False)
    smart_price_value = models.FloatField(default=0.0)
    # 1 for EUR
    # 2 for USD
    # 3 for CNY
    # 4 for RON
    currency_code = models.IntegerField(default=0)
    margin_whole_sale = models.FloatField(default=0.0)
    margin_whole_sale_unit = models.IntegerField(default=0)
    whole_sale_price = models.FloatField(default=0.0)
    margin_retail = models.FloatField(default=0.0)
    margin_retail_unit = models.IntegerField(default=0)
    retail_price = models.FloatField(default=0.0)
    old_retail_price = models.FloatField(default=0.0)
    old_retail_date = models.DateField(null=True)
    local_cost = models.FloatField(default=0.0)
    thenx_cost = models.FloatField(default=0.0)
    supplier_price_ron = models.FloatField(default=0.0)
    exchange_rate = models.FloatField(default=0.0)
    all_cost_price = models.FloatField(default=0.0)
    old_all_cost_price = models.FloatField(default=0.0)
    old_all_cost_date = models.DateField(null=True)
    cheapest_comp = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now_add=True)


class ProductCalculationInformation(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    local_cost_supplier = models.FloatField(default=0.0)
    thenx_cost_supplier = models.FloatField(default=0.0)
    all_cost_price = models.FloatField(default=0.0)
    whole_sale_margin = models.FloatField(default=0)
    retail_margin = models.FloatField(default=0)
    whole_sale_price = models.FloatField(default=0.0)
    gross_profit_whole_sale = models.FloatField(default=0.0)
    retail_sale_price = models.FloatField(default=0.0)
    gross_profit_retail_sale = models.FloatField(default=0.0)
    vat = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductCalculationInformationFormulas(models.Model):
    pro_cal_info = models.ForeignKey(ProductCalculationInformation, on_delete=models.CASCADE)
    local_cost_value = models.FloatField(default=0.0)
    # 1 for ron
    # 2 for percentage
    local_cost_price_type = models.IntegerField(default=1)
    thenx_cost_value = models.FloatField(default=0.0)
    # 1 for ron
    # 2 for percentage
    thenx_cost_price_type = models.IntegerField(default=1)
    whole_sale_price = models.FloatField(default=0.0)
    # 1 for ron
    # 2 for percentage
    whole_sale_price_type = models.IntegerField(default=1)
    retail_sale_price = models.FloatField(default=0.0)
    # 1 for ron
    # 2 for percentage
    retail_sale_price_type = models.IntegerField(default=1)


class ProductCompetitorSites(models.Model):
    reference_id = models.IntegerField(default=0)
    name = models.TextField(default='')


class ProductCompetitorsLinks(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    site_reference = models.ForeignKey(ProductCompetitorSites, on_delete=models.CASCADE)
    link = models.TextField(default='')


class SupplierDetailPrices(models.Model):
    supplier = models.ForeignKey(Suppliers, on_delete=models.CASCADE, null=True)
    local_cost = models.FloatField(default=LOCAL_COST_OF_SUPPLIER_IN_PERCENTAGE)
    local_cost_thenx = models.FloatField(default=LOCAL_COST_OF_THENX_IN_PERCENTAGE)
    vat_price = models.FloatField(default=LOCAL_COST_OF_THENX_IN_PERCENTAGE)
    whole_sale_price_margin = models.FloatField(default=0.0)
    retail_sale_price_margin = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Rules(models.Model):
    # 1 for setting warranty price
    # 2 for setting vat price
    # 3 for setting margin rule
    # 4 for setting local cost
    # 5 for setting thenx cost
    # 6 for setting competitor rule
    rule_type = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class WarrantyRule(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    # no of days
    days = models.IntegerField(default=1)
    is_all_suppliers = models.BooleanField(default=False)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Suppliers)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class VatRule(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    percentage = models.FloatField(default=0)


class MarginRules(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    # for higher check
    price_dependancy = models.FloatField(default=0)
    # for lower check
    price_dependancy2 = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    # 1 for ron
    # 2 for percentage
    percentage_unit = models.IntegerField(default=2)
    higher_percentage = models.FloatField(default=0)
    higher_percentage_unit = models.IntegerField(default=2)
    lower_percentage = models.FloatField(default=0)
    lower_percentage_unit = models.IntegerField(default=2)
    # 0 for whole sale price
    # 1 for retail price
    type = models.IntegerField(default=0)
    is_all_suppliers = models.BooleanField(default=False)
    supplier = models.ManyToManyField(Suppliers)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class MarginRulesReferenceModel(models.Model):
    percentage = models.FloatField(default=0)
    # 1 for ron
    # 2 for percentage
    percentage_unit = models.IntegerField(default=2)
    # 0 for whole sale price
    # 1 for retail price
    type = models.IntegerField(default=0)
    is_all_suppliers = models.BooleanField(default=False)
    supplier = models.ManyToManyField(Suppliers)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class LocalCostSupplier(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    cost = models.FloatField(default=0)
    cost_unit = models.IntegerField(default=1)
    percentage = models.FloatField(default=0.0)
    percentage_unit = models.IntegerField(default=1)
    price_dependancey = models.FloatField(default=0.0)
    # True for higher check with cost
    # False for lower check with percentage
    supplier_price_higher_check = models.BooleanField(default=False)
    is_all_suppliers = models.BooleanField(default=False)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Suppliers)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class ThenxCostSupplier(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    cost = models.FloatField(default=0)
    percentage = models.FloatField(default=0.0)
    price_dependancey = models.FloatField(default=0.0)
    cost_unit = models.IntegerField(default=1)
    percentage_unit = models.IntegerField(default=1)
    # True for higher check with cost
    # False for lower check with cost
    supplier_price_higher_check = models.BooleanField(default=False)
    is_all_suppliers = models.BooleanField(default=False)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Suppliers)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class PriceCompetitorRule(models.Model):
    rule = models.ForeignKey(Rules, on_delete=models.CASCADE)
    check_pricer = models.FloatField(default=0)
    # 1 for ron
    # 2 for percentage
    check_pricer_unit = models.IntegerField(default=1)
    # 1 for higher
    # 2 for lower
    check_pricer_priority = models.IntegerField(default=1)
    # 1 for highest
    # 2 for average
    # 3 for lowest
    competitor_priority = models.IntegerField(default=1)
    competitor = models.ForeignKey(ProductCompetitorSites, on_delete=models.CASCADE, null=True)
    is_all_competitors = models.BooleanField(default=False)
    final_price_check = models.FloatField(default=0)
    # 1 for ron
    # 2 for percentage
    final_price_unit = models.IntegerField(default=1)
    is_all_suppliers = models.BooleanField(default=False)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Suppliers)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class PriceCompetitorRuleReferenceModel(models.Model):
    check_pricer = models.FloatField(default=0)
    # 1 for ron
    # 2 for percentage
    check_pricer_unit = models.IntegerField(default=1)
    # 1 for higher
    # 2 for lower
    check_pricer_priority = models.IntegerField(default=1)
    # 1 for highest
    # 2 for average
    # 3 for lowest
    competitor_priority = models.IntegerField(default=1)
    competitor = models.ForeignKey(ProductCompetitorSites, on_delete=models.CASCADE, null=True)
    is_all_competitors = models.BooleanField(default=False)
    final_price_check = models.FloatField(default=0)
    # 1 for ron
    # 2 for percentage
    final_price_unit = models.IntegerField(default=1)
    is_all_suppliers = models.BooleanField(default=False)
    is_all_categories = models.BooleanField(default=False)
    is_on_product = models.BooleanField(default=False)
    # True for category check
    # False for product check
    is_on_category = models.BooleanField(default=True)
    supplier = models.ManyToManyField(Suppliers)
    category = models.ManyToManyField(Categories)
    product_sku = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)


class ProductCompetitorSitesReference(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    competitor_link = models.ForeignKey(ProductCompetitorsLinks, on_delete=models.CASCADE, null=True)
    site_reference = models.ForeignKey(ProductCompetitorSites, on_delete=models.CASCADE, null=True)
    link = models.TextField(default='')
    old_price = models.TextField(default='')
    old_price_date = models.DateField(null=True)
    comp_price = models.TextField(default='')
    promotion_price = models.TextField(default='')
    stock_entry = models.TextField(default='')
    # True for error
    # False for error
    is_error = models.BooleanField(default=False)
    error_information = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class CronJobLogRunning(models.Model):
    # 0 for fetching product information
    # 1 for fetching product competitor prices
    # 2 for competitor links fetching jobs
    # 3 for fetching new products of competitors
    # 4 for fetching product competitor without competitor
    cron_job_type = models.IntegerField(default=0)
    scanned_sku = models.IntegerField(default=0)
    changed_prices = models.IntegerField(default=0)
    new_sku = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class LogErrorWhileScraping(models.Model):
    site_name = models.TextField(default='')
    link = models.TextField(default='')
    site_reference = models.ForeignKey(ProductCompetitorSites, on_delete=models.CASCADE, null=True)
    exception = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class AdminLogOfJobToShow(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_sku = models.TextField(default='')
    product_cost = models.FloatField(default=0.0)
    all_cost_price = models.FloatField(default=0.0)
    competitor_site_log = models.ManyToManyField(ProductCompetitorSitesReference)
    # 0 for N/A
    # 1 for highest
    # 2 for higher
    # 3 for average
    # 4 for cheaper
    # 5 for Cheapest
    # 6 for All Equal
    rank_of_product = models.IntegerField(default=0)
    total_competitors_link = models.IntegerField(default=0)
    cheapest_price = models.FloatField(default=0)
    highest_price = models.FloatField(default=0)
    average_price = models.FloatField(default=0)
    cheapest_price_text = models.TextField(default='')
    highest_price_text = models.TextField(default='')
    average_price_text = models.TextField(default='')
    product_price = models.FloatField(default=0.0)
    expected_price = models.FloatField(default=0.0)
    same_moment_calculated_price = models.FloatField(default=0.0)
    # 1 for same
    # 2 for exceeded
    # 3 for decreased
    price_change_effect = models.IntegerField(default=0)
    # False for disapproved
    is_approved = models.BooleanField(default=False)
    is_competitor_less_than_cost = models.BooleanField(default=False)
    is_competitor_rule_applied = models.BooleanField(default=False)
    is_margin_rule_applied = models.BooleanField(default=False)
    margin_rule_identity = models.ForeignKey(MarginRulesReferenceModel, on_delete=models.CASCADE, null=True)
    is_original_price_applied = models.BooleanField(default=False)
    competitor_rule_identity = models.ForeignKey(PriceCompetitorRuleReferenceModel, on_delete=models.CASCADE, null=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    is_price_change = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=True)
    # is without competitor
    is_competitor_asscoiated = models.BooleanField(default=False)
    is_smart_price_set_applied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class UsersPermissions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_home_page = models.BooleanField(default=False)
    is_products_page = models.BooleanField(default=False)
    is_rules_page = models.BooleanField(default=False)
    is_competitors_page = models.BooleanField(default=False)
    is_daily_price_page = models.BooleanField(default=False)
    is_active_links_page = models.BooleanField(default=False)
    is_cron_job_logs_page = models.BooleanField(default=False)
    is_remove = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class WeeklyReportNewProducts(models.Model):
    total_new_products = models.IntegerField(default=0)
    service_pack_new_products = models.IntegerField(default=0)
    magazingsm_new_products = models.IntegerField(default=0)
    portableta_new_products = models.IntegerField(default=0)
    moka_gsm_new_products = models.IntegerField(default=0)
    sunnex_new_products = models.IntegerField(default=0)
    sep_mobile_new_products = models.IntegerField(default=0)
    gsmnet_new_products = models.IntegerField(default=0)
    distrizone_new_products = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class InstantJobDeclaration(models.Model):
    # 0 for competitors
    # 1 for new products
    # 2 for product competitors job
    job_type = models.IntegerField(default=0)
    competitor = models.IntegerField(default=0)
    supplier = models.IntegerField(default=0)
    category = models.IntegerField(default=0)
    product_list = models.TextField(default='')
    # 0 for job started
    # 1 for job completed
    status = models.IntegerField(default=0)
    products_price_changes = models.IntegerField(default=0)
    status_of_job = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
