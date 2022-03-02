from .models import *


class EditRule:
    def __init__(self, request, rule):
        self.request = request.POST
        self.rule = rule

    def add_warranty_rule(self):
        warranty_days = int(self.request['warranty_days']) if 'warranty_days' in self.request else 10
        # warranty_suppliers = int(self.request['warranty_suppliers']) if 'warranty_suppliers' in self.request else 0
        # warranty_category = self.request['warranty_category'] if 'warranty_category' in self.request else ''
        # warranty_product_sku = self.request['warranty_product_sku'] if 'warranty_product_sku' in self.request else ''

        # if warranty_category:
        #     warranty_category = [int(x) for x in warranty_category.split(',')]
        #     is_category_info = True
        #     if 0 in warranty_category:
        #         is_all_categories = True
        #
        # if warranty_product_sku:
        #     product_ = Products.objects.filter(sku=warranty_product_sku).last()
        #     if not product_:
        #         return

        rule_ = self.rule
        rule_ = WarrantyRule.objects.get(rule=rule_)
        rule_.days = warranty_days

        # if warranty_suppliers == 0:
        #     rule_.supplier.add(*[x for x in Suppliers.objects.all()])
        #     rule_.is_all_suppliers = True
        # else:
        #     supplier_ = Suppliers.objects.get(id=warranty_suppliers)
        #     rule_.supplier.add(supplier_)
        #     rule_.is_all_suppliers = False
        #
        # if warranty_category:
        #     rule_.is_on_category = True
        #     if 0 in warranty_category:
        #         rule_.category.add(*[x for x in Categories.objects.all()])
        #         rule_.is_all_categories = True
        #     else:
        #         rule_.category.add(*[Categories.objects.get(id=int(x)) for x in warranty_category])
        #         rule_.is_all_categories = False
        # else:
        #     pro_ = Products.objects.get(sku=warranty_product_sku)
        #     rule_.product_sku = pro_
        #     rule_.is_on_category = False
        rule_.save()

    def add_margin_rule(self):
        margin_type = int(self.request['margin_type']) if 'margin_type' in self.request else 0
        margin_price = float(self.request['margin_price']) if 'margin_price' in self.request else 0
        # margin_supplier = int(self.request['margin_supplier']) if 'margin_supplier' in self.request else 0
        margin_price_unit = int(self.request['margin_price_unit']) if 'margin_price_unit' in self.request else 0
        # margin_category = self.request['margin_category'] if 'margin_category' in self.request else ''
        # margin_product_sku = self.request['margin_product_sku'] if 'margin_product_sku' in self.request else ''

        price_dependancy2 = float(self.request['price_dependancy2']) if 'price_dependancy2' in self.request else 0
        lower_percentage = float(self.request['lower_percentage']) if 'lower_percentage' in self.request else 0
        lower_percentage_unit_int = int(self.request['lower_percentage_unit_int']) if 'lower_percentage_unit_int' in self.request else 0
        price_dependancy = float(self.request['price_dependancy']) if 'price_dependancy' in self.request else 0
        higher_percentage_unit_int = int(self.request['higher_percentage_unit_int']) if 'higher_percentage_unit_int' in self.request else 0
        higher_percentage = float(self.request['higher_percentage']) if 'higher_percentage' in self.request else 0

        # if margin_category:
        #     margin_category = [int(x) for x in margin_category.split(',')]
        #     is_category_info = True
        #     if 0 in margin_category:
        #         is_all_categories = True
        #
        # if margin_product_sku:
        #     product_ = Products.objects.filter(sku=margin_product_sku).last()
        #     if not product_:
        #         return

        rule_ = self.rule
        rule_ = MarginRules.objects.get(rule=rule_)
        rule_.percentage = margin_price
        rule_.type = margin_type
        rule_.percentage_unit = margin_price_unit

        rule_.higher_percentage = higher_percentage
        rule_.higher_percentage_unit = higher_percentage_unit_int
        rule_.price_dependancy = price_dependancy

        rule_.lower_percentage = lower_percentage
        rule_.lower_percentage_unit = lower_percentage_unit_int
        rule_.price_dependancy2 = price_dependancy2

        # if margin_supplier == 0:
        #     rule_.supplier.add(*[x for x in Suppliers.objects.all()])
        #     rule_.is_all_suppliers = True
        # else:
        #     supplier_ = Suppliers.objects.get(id=margin_supplier)
        #     rule_.supplier.add(supplier_)
        #     rule_.is_all_suppliers = False
        #
        # if margin_category:
        #     rule_.is_on_category = True
        #     if 0 in margin_category:
        #         rule_.category.add(*[x for x in Categories.objects.all()])
        #         rule_.is_all_categories = True
        #     else:
        #         rule_.category.add(*[Categories.objects.get(id=int(x)) for x in margin_category])
        #         rule_.is_all_categories = False
        # else:
        #     pro_ = Products.objects.get(sku=margin_product_sku)
        #     rule_.product_sku = pro_
        #     rule_.is_on_category = False
        rule_.save()

    def add_price_competitor_rule(self):
        competitor_price = float(self.request['competitor_price']) if 'competitor_price' in self.request else 0
        competitor_price_type = self.request['competitor_price_type'] if 'competitor_price_type' in self.request else 1
        competitor_price_first_priority = float(
            self.request['competitor_price_first_priority']) if 'competitor_price_first_priority' in self.request else 1
        competitor_price_second_priority = int(self.request[
                                                   'competitor_price_second_priority']) if 'competitor_price_second_priority' in self.request else 1
        competitor_competitor_select = int(
            self.request['competitor_competitor_select']) if 'competitor_competitor_select' in self.request else None
        competitor_cost = float(self.request['competitor_cost']) if 'competitor_cost' in self.request else 0
        competitor_cost_type = int(
            self.request['competitor_cost_type']) if 'competitor_cost_type' in self.request else 1

        # competitor_supplier = int(self.request['competitor_supplier']) if 'competitor_supplier' in self.request else 0
        # competitor_category = self.request['competitor_category'] if 'competitor_category' in self.request else ''
        # competitor_product_sku = self.request[
        #     'competitor_product_sku'] if 'competitor_product_sku' in self.request else ''

        # if competitor_category:
        #     competitor_category = [int(x) for x in competitor_category.split(',')]
        #     is_category_info = True
        #     if 0 in competitor_category:
        #         is_all_categories = True
        #
        # if competitor_product_sku:
        #     product_ = Products.objects.filter(sku=competitor_product_sku).last()
        #     if not product_:
        #         return

        rule_ = Rules.objects.get(rule_type=6)
        rule_ = PriceCompetitorRule.objects.get(rule=rule_)
        rule_.check_pricer = competitor_price
        rule_.check_pricer_unit = competitor_price_type
        rule_.check_pricer_priority = competitor_price_first_priority
        rule_.competitor_priority = competitor_price_second_priority
        rule_.final_price_check = competitor_cost
        rule_.final_price_unit = competitor_cost_type

        if competitor_competitor_select == 0:
            rule_.is_all_competitors = True
        else:
            competitor = ProductCompetitorSites.objects.get(id=competitor_competitor_select)
            rule_.is_all_competitors = False
            rule_.competitor = competitor

        # if competitor_supplier == 0:
        #     rule_.supplier.add(*[x for x in Suppliers.objects.all()])
        #     rule_.is_all_suppliers = True
        # else:
        #     supplier_ = Suppliers.objects.get(id=competitor_supplier)
        #     rule_.supplier.add(supplier_)
        #     rule_.is_all_suppliers = False
        #
        # if competitor_category:
        #     rule_.is_on_category = True
        #     if 0 in competitor_category:
        #         rule_.category.add(*[x for x in Categories.objects.all()])
        #         rule_.is_all_categories = True
        #     else:
        #         rule_.category.add(*[Categories.objects.get(id=int(x)) for x in competitor_category])
        #         rule_.is_all_categories = False
        # else:
        #     pro_ = Products.objects.get(sku=competitor_product_sku)
        #     rule_.product_sku = pro_
        #     rule_.is_on_category = False
        rule_.save()

    def add_local_cost_supplier_rule(self):
        local_cost_price = self.request['local_cost_price']
        local_cost_price_unit = self.request['local_cost_price_unit']
        local_cost_price_competitor = self.request['local_cost_price_competitor']
        local_cost_price_percentage = self.request['local_cost_price_percentage']
        local_cost_price_percentage_unit = self.request['local_cost_price_percentage_unit']

        rule_ = LocalCostSupplier.objects.get(rule=self.rule)
        rule_.supplier_price_higher_check = True
        rule_.cost = local_cost_price
        rule_.cost_unit = local_cost_price_unit
        rule_.price_dependancey = local_cost_price_competitor
        rule_.percentage = local_cost_price_percentage
        rule_.percentage_unit = local_cost_price_percentage_unit
        rule_.save()

    def add_thenx_cost_supplier_rule(self):
        thenx_cost_price = self.request['thenx_cost_price']
        thenx_cost_price_competitor = self.request['thenx_cost_price_competitor']
        thenx_cost_price_percentage = self.request['thenx_cost_price_percentage']
        # thenx_cost_supplier = int(self.request['thenx_cost_supplier'])
        # thenx_cost_category = self.request['thenx_cost_category']
        # thenx_cost_product_sku = self.request['thenx_cost_product_sku']
        thenx_cost_price_unit = self.request['thenx_cost_price_unit']
        thenx_cost_price_percentage_unit = self.request['thenx_cost_price_percentage_unit']

        # if thenx_cost_category:
        #     thenx_cost_category = [int(x) for x in thenx_cost_category.split(',')]
        #     is_category_info = True
        #     if 0 in thenx_cost_category:
        #         is_all_categories = True
        #
        # if thenx_cost_product_sku:
        #     product_ = Products.objects.filter(sku=thenx_cost_product_sku).last()
        #     if not product_:
        #         return

        rule_ = ThenxCostSupplier.objects.get(rule=self.rule)
        rule_.supplier_price_higher_check = True
        rule_.cost = thenx_cost_price
        rule_.price_dependancey = thenx_cost_price_competitor
        rule_.percentage = thenx_cost_price_percentage
        rule_.percentage_unit = thenx_cost_price_percentage_unit
        rule_.cost_unit = thenx_cost_price_unit
        rule_.save()

        # if thenx_cost_supplier == 0:
        #     rule_.supplier.add(*[x for x in Suppliers.objects.all()])
        #     rule_.is_all_suppliers = True
        # else:
        #     supplier_ = Suppliers.objects.get(id=thenx_cost_supplier)
        #     rule_.supplier.add(supplier_)
        #     rule_.is_all_suppliers = False
        #
        # if thenx_cost_category:
        #     rule_.is_on_category = True
        #     if 0 in thenx_cost_category:
        #         rule_.category.add(*[x for x in Categories.objects.all()])
        #         rule_.is_all_categories = True
        #     else:
        #         rule_.category.add(*[Categories.objects.get(id=int(x)) for x in thenx_cost_category])
        #         rule_.is_all_categories = False
        # else:
        #     pro_ = Products.objects.get(sku=thenx_cost_product_sku)
        #     rule_.product_sku = pro_
        #     rule_.is_on_category = False
        rule_.save()
