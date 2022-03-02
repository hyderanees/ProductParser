from .models import *


class Rule:
    def __init__(self, request):
        self.request = request.POST

    def add_warranty_rule(self):
        warranty_days = int(self.request['warranty_days']) if 'warranty_days' in self.request else 10
        warranty_suppliers = int(self.request['warranty_suppliers']) if 'warranty_suppliers' in self.request else 0
        warranty_category = self.request['warranty_category'] if 'warranty_category' in self.request else ''
        warranty_product_sku = self.request['warranty_product_sku'] if 'warranty_product_sku' in self.request else ''

        is_supplier_exists = False
        is_category_info = False
        is_all_categories = False
        wr = None

        if warranty_category:
            warranty_category = [int(x) for x in warranty_category.split(',')]
            is_category_info = True
            if 0 in warranty_category:
                is_all_categories = True

        if warranty_product_sku:
            product_ = Products.objects.filter(sku=warranty_product_sku).last()
            if not product_:
                return

        # Rules validation to stop duplication
        if warranty_suppliers != 0 and is_category_info == True and is_all_categories == True:
            if WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
                                           is_all_categories=True).exists():
                is_supplier_exists = True
                wr = WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
                                                 is_all_categories=True).last()
        #
        # if warranty_suppliers != 0 and is_category_info == True and is_all_categories == False:
        #     if WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
        #                                    category__id__in=warranty_category).exists():
        #         is_supplier_exists = False
        #         wr = WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
        #                                          category__id__in=warranty_category)
        #         for obj in wr:
        #             for x in warranty_category:
        #                 obj.category.remove(Categories.objects.get(id=x))
        #             if obj.category.all().count() < 1:
        #                 rule_ = obj.rule
        #                 rule_.delete()
        #                 obj.delete()
        #
        if warranty_suppliers != 0 and is_category_info == False:
            if WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
                                           product_sku__sku=warranty_product_sku).exists():
                is_supplier_exists = True
                wr = WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
                                                 product_sku__sku=warranty_product_sku).last()

        if warranty_suppliers == 0 and is_category_info == True and is_all_categories == True:
            if WarrantyRule.objects.filter(is_all_suppliers=True, is_all_categories=True).exists():
                is_supplier_exists = True
                wr = WarrantyRule.objects.filter(is_all_suppliers=True, is_all_categories=True).last()
        #
        # if warranty_suppliers == 0 and is_category_info == True and is_all_categories == False:
        #     if WarrantyRule.objects.filter(is_all_suppliers=True, category__id__in=warranty_category).exists():
        #         is_supplier_exists = False
        #         wr = WarrantyRule.objects.filter(is_all_suppliers=True, category__id__in=warranty_category).last()
        #         for obj in wr:
        #             for x in warranty_category:
        #                 obj.category.remove(Categories.objects.get(id=x))
        #             if obj.category.all().count() < 1:
        #                 rule_ = obj.rule
        #                 rule_.delete()
        #                 obj.delete()
        #
        if warranty_suppliers == 0 and is_category_info == False:
            if WarrantyRule.objects.filter(is_all_suppliers=False, supplier__reference_id=warranty_suppliers,
                                           product_sku__sku=warranty_product_sku).exists():
                is_supplier_exists = True
                wr = WarrantyRule.objects.filter(is_all_suppliers=True, product_sku__sku=warranty_product_sku).last()

        if not is_supplier_exists:
            rule_ = Rules.objects.create(rule_type=1)
            rule_ = WarrantyRule.objects.create(rule=rule_, days=warranty_days)

            if warranty_suppliers == 0:
                rule_.supplier.add(*[x for x in Suppliers.objects.all()])
                rule_.is_all_suppliers = True
            else:
                supplier_ = Suppliers.objects.get(id=warranty_suppliers)
                rule_.supplier.add(supplier_)
                rule_.is_all_suppliers = False

            if warranty_category:
                rule_.is_on_category = True
                if 0 in warranty_category:
                    rule_.category.add(*[x for x in Categories.objects.all()])
                    rule_.is_all_categories = True
                else:
                    rule_.category.add(*[Categories.objects.get(id=int(x)) for x in warranty_category])
                    rule_.is_all_categories = False
            else:
                pro_ = Products.objects.get(sku=warranty_product_sku)
                rule_.product_sku = pro_
                rule_.is_on_category = False
            rule_.save()
        else:
            wr.days = warranty_days
            wr.save()

    def add_margin_rule(self):
        margin_type = int(self.request['margin_type']) if 'margin_type' in self.request else 0
        margin_price = float(self.request['margin_price']) if 'margin_price' in self.request else 0
        margin_supplier = int(self.request['margin_supplier']) if 'margin_supplier' in self.request else 0
        margin_price_unit = int(self.request['margin_price_unit']) if 'margin_price_unit' in self.request else 0
        margin_price2 = float(self.request['margin_price2']) if 'margin_price2' in self.request else 0
        margin_price2_unit = int(self.request['margin_price_unit2']) if 'margin_price_unit2' in self.request else 0
        margin_price3 = float(self.request['margin_price3']) if 'margin_price3' in self.request else 0
        margin_price3_unit = int(self.request['margin_price_unit3']) if 'margin_price_unit3' in self.request else 0
        margin_category = self.request['margin_category'] if 'margin_category' in self.request else ''
        margin_product_sku = self.request['margin_product_sku'] if 'margin_product_sku' in self.request else ''
        price_dependancy2 = float(self.request['price_dependancy']) if 'price_dependancy' in self.request else 0
        price_dependancy = float(self.request['price_dependancy2']) if 'price_dependancy2' in self.request else 0

        is_category_info = False
        is_all_categories = False
        is_supplier_exists = False

        if margin_category:
            margin_category = [int(x) for x in margin_category.split(',')]
            is_category_info = True
            if 0 in margin_category:
                is_all_categories = True

        if margin_product_sku:
            product_ = Products.objects.filter(sku=margin_product_sku).last()
            if not product_:
                return

        # Rules validation to stop duplication
        if margin_supplier != 0 and is_category_info == True and is_all_categories == True:
            if MarginRules.objects.filter(is_all_suppliers=False,
                                          type=margin_type,
                                          supplier__reference_id=margin_supplier,
                                          is_all_categories=True).exists():
                is_supplier_exists = True
                mr = MarginRules.objects.filter(is_all_suppliers=False,
                                                type=margin_type,
                                                supplier__reference_id=margin_supplier,
                                                is_all_categories=True).last()

        if margin_supplier != 0 and is_category_info == False:
            if MarginRules.objects.filter(is_all_suppliers=False,
                                          type=margin_type,
                                          supplier__reference_id=margin_supplier,
                                          is_on_category=False,
                                          product_sku__sku=margin_product_sku).exists():
                is_supplier_exists = True
                mr = MarginRules.objects.filter(is_all_suppliers=False, type=margin_type,
                                                supplier__reference_id=margin_supplier,
                                                is_on_category=False,
                                                product_sku__sku=margin_product_sku).last()

        if margin_supplier == 0 and is_category_info == True and is_all_categories == True:
            if MarginRules.objects.filter(is_all_suppliers=True, is_all_categories=True, type=margin_type).exists():
                is_supplier_exists = True
                mr = MarginRules.objects.filter(is_all_suppliers=True, is_all_categories=True, type=margin_type).last()

        if margin_supplier == 0 and is_category_info == False:
            if MarginRules.objects.filter(is_all_suppliers=True, is_on_category=False,
                                          type=margin_type,
                                          product_sku__sku=margin_product_sku).exists():
                is_supplier_exists = True
                mr = MarginRules.objects.filter(is_all_suppliers=True, is_on_category=False,
                                                type=margin_type,
                                                product_sku__sku=margin_product_sku).last()

        if not is_supplier_exists:
            rule_ = Rules.objects.create(rule_type=3)
            rule_ = MarginRules.objects.create(rule=rule_, percentage=margin_price, type=margin_type,
                                               percentage_unit=margin_price_unit,
                                               price_dependancy=price_dependancy,
                                               price_dependancy2=price_dependancy2,
                                               higher_percentage=margin_price3,
                                               higher_percentage_unit=margin_price3_unit,
                                               lower_percentage=margin_price2,
                                               lower_percentage_unit=margin_price2_unit)

            if margin_supplier == 0:
                rule_.supplier.add(*[x for x in Suppliers.objects.all()])
                rule_.is_all_suppliers = True
            else:
                supplier_ = Suppliers.objects.get(id=margin_supplier)
                rule_.supplier.add(supplier_)
                rule_.is_all_suppliers = False

            if margin_category:
                rule_.is_on_category = True
                if 0 in margin_category:
                    rule_.category.add(*[x for x in Categories.objects.all()])
                    rule_.is_all_categories = True
                else:
                    rule_.category.add(*[Categories.objects.get(id=int(x)) for x in margin_category])
                    rule_.is_all_categories = False
            else:
                pro_ = Products.objects.get(sku=margin_product_sku)
                rule_.product_sku = pro_
                rule_.is_on_category = False
            rule_.save()
        else:
            mr.percentage = margin_price
            mr.price_dependancy = price_dependancy
            mr.price_dependancy2 = price_dependancy2
            mr.percentage_unit = margin_price_unit
            mr.higher_percentage = margin_price3
            mr.higher_percentage_unit = margin_price3_unit
            mr.lower_percentage = margin_price2
            mr.lower_percentage_unit = margin_price2_unit
            mr.save()

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

        competitor_supplier = int(self.request['competitor_supplier']) if 'competitor_supplier' in self.request else 0
        competitor_category = self.request['competitor_category'] if 'competitor_category' in self.request else ''
        competitor_product_sku = self.request[
            'competitor_product_sku'] if 'competitor_product_sku' in self.request else ''

        is_category_info = False
        is_all_categories = False
        is_supplier_exists = False

        if competitor_category:
            competitor_category = [int(x) for x in competitor_category.split(',')]
            is_category_info = True
            if 0 in competitor_category:
                is_all_categories = True

        if competitor_product_sku:
            product_ = Products.objects.filter(sku=competitor_product_sku).last()
            if not product_:
                return

        is_obj_exists = False
        if competitor_competitor_select == 0:
            if PriceCompetitorRule.objects.filter(is_all_competitors=True).exists():
                is_obj_exists = True
                obj = PriceCompetitorRule.objects.filter(is_all_competitors=True)
        else:
            competitor = ProductCompetitorSites.objects.get(id=competitor_competitor_select)
            if PriceCompetitorRule.objects.filter(is_all_competitors=False, competitor=competitor).exists():
                is_obj_exists = True
                obj = PriceCompetitorRule.objects.filter(is_all_competitors=False, competitor=competitor)

        if is_obj_exists:
            if competitor_supplier != 0 and is_category_info == True and is_all_categories == True:
                if obj.filter(is_all_suppliers=False,
                              supplier__reference_id=competitor_supplier,
                              is_all_categories=True).exists():
                    is_supplier_exists = True
                    competitor__ = obj.filter(is_all_suppliers=False,
                                              supplier__reference_id=competitor_supplier,
                                              is_all_categories=True).last()

            if competitor_supplier != 0 and is_category_info == False:
                if obj.filter(is_all_suppliers=False,
                              supplier__reference_id=competitor_supplier,
                              is_on_category=False,
                              product_sku__sku=competitor_product_sku).exists():
                    is_supplier_exists = True
                    competitor__ = obj.filter(is_all_suppliers=False,
                                              supplier__reference_id=competitor_supplier,
                                              is_on_category=False,
                                              product_sku__sku=competitor_product_sku).last()

            if competitor_supplier == 0 and is_category_info == True and is_all_categories == True:
                if obj.filter(is_all_suppliers=True, is_all_categories=True).exists():
                    is_supplier_exists = True
                    competitor__ = obj.filter(is_all_suppliers=True, is_all_categories=True).last()

            if competitor_supplier == 0 and is_category_info == False:
                if obj.filter(is_all_suppliers=True, is_on_category=False,
                              product_sku__sku=competitor_product_sku).exists():
                    is_supplier_exists = True
                    competitor__ = obj.filter(is_all_suppliers=True, is_on_category=False,
                                              product_sku__sku=competitor_product_sku).last()

        if not is_supplier_exists:
            rule_ = Rules.objects.create(rule_type=6)
            rule_ = PriceCompetitorRule.objects.create(rule=rule_, check_pricer=competitor_price,
                                                       check_pricer_unit=competitor_price_type,
                                                       check_pricer_priority=competitor_price_first_priority,
                                                       competitor_priority=competitor_price_second_priority,
                                                       final_price_check=competitor_cost,
                                                       final_price_unit=competitor_cost_type)
            if competitor_competitor_select == 0:
                rule_.is_all_competitors = True
            else:
                competitor = ProductCompetitorSites.objects.get(id=competitor_competitor_select)
                rule_.is_all_competitors = False
                rule_.competitor = competitor

            if competitor_supplier == 0:
                rule_.supplier.add(*[x for x in Suppliers.objects.all()])
                rule_.is_all_suppliers = True
            else:
                supplier_ = Suppliers.objects.get(id=competitor_supplier)
                rule_.supplier.add(supplier_)
                rule_.is_all_suppliers = False

            if competitor_category:
                rule_.is_on_category = True
                if 0 in competitor_category:
                    rule_.category.add(*[x for x in Categories.objects.all()])
                    rule_.is_all_categories = True
                else:
                    rule_.category.add(*[Categories.objects.get(id=int(x)) for x in competitor_category])
                    rule_.is_all_categories = False
            else:
                pro_ = Products.objects.get(sku=competitor_product_sku)
                rule_.product_sku = pro_
                rule_.is_on_category = False
            rule_.save()
        else:
            competitor__.check_pricer = competitor_price
            competitor__.check_pricer_unit = competitor_price_type
            competitor__.check_pricer_priority = competitor_price_first_priority
            competitor__.competitor_priority = competitor_price_second_priority
            competitor__.final_price_check = competitor_cost
            competitor__.final_price_unit = competitor_cost_type

            if competitor_competitor_select == 0:
                competitor__.is_all_competitors = True
            else:
                competitor = ProductCompetitorSites.objects.get(id=competitor_competitor_select)
                competitor__.is_all_competitors = False
                competitor__.competitor = competitor

            competitor__.save()

    def add_local_cost_supplier_rule(self):
        local_cost_price = self.request['local_cost_price']
        local_cost_price_unit = self.request['local_cost_price_unit']
        local_cost_price_competitor = self.request['local_cost_price_competitor']
        local_cost_price_percentage = self.request['local_cost_price_percentage']
        local_cost_price_percentage_unit = self.request['local_cost_price_percentage_unit']
        local_cost_supplier = int(self.request['local_cost_supplier'])
        local_cost_category = self.request['local_cost_category'] if 'local_cost_category' in self.request else ''
        local_cost_product_sku = self.request['local_cost_product_sku']

        is_supplier_exists = False
        is_category_info = False
        is_all_categories = False

        if local_cost_category:
            local_cost_category = [int(x) for x in local_cost_category.split(',')]
            is_category_info = True
            if 0 in local_cost_category:
                is_all_categories = True

        if local_cost_product_sku:
            product_ = Products.objects.filter(sku=local_cost_product_sku).last()
            if not product_:
                return

        # Rules validation to stop duplication
        if local_cost_supplier != 0 and is_category_info == True and is_all_categories == True:
            if LocalCostSupplier.objects.filter(is_all_suppliers=False, supplier__reference_id=local_cost_supplier,
                                                is_all_categories=True).exists():
                is_supplier_exists = True
                lcp = LocalCostSupplier.objects.filter(is_all_suppliers=False,
                                                       supplier__reference_id=local_cost_supplier,
                                                       is_all_categories=True).last()

        if local_cost_supplier != 0 and is_category_info == False:
            if LocalCostSupplier.objects.filter(is_all_suppliers=False, supplier__reference_id=local_cost_supplier,
                                                is_on_category=False,
                                                product_sku__sku=local_cost_product_sku).exists():
                is_supplier_exists = True
                lcp = LocalCostSupplier.objects.filter(is_all_suppliers=False,
                                                       supplier__reference_id=local_cost_supplier,
                                                       is_on_category=False,
                                                       product_sku__sku=local_cost_product_sku).last()

        if local_cost_supplier == 0 and is_category_info == True and is_all_categories == True:
            if LocalCostSupplier.objects.filter(is_all_suppliers=True, is_all_categories=True).exists():
                is_supplier_exists = True
                lcp = LocalCostSupplier.objects.filter(is_all_suppliers=True, is_all_categories=True).last()

        if local_cost_supplier == 0 and is_category_info == False:
            if LocalCostSupplier.objects.filter(is_all_suppliers=True, is_on_category=False,
                                                product_sku__sku=local_cost_product_sku).exists():
                is_supplier_exists = True
                lcp = LocalCostSupplier.objects.filter(is_all_suppliers=True, is_on_category=False,
                                                       product_sku__sku=local_cost_product_sku).last()

        if not is_supplier_exists:
            rule_ = Rules.objects.create(rule_type=4)
            rule_ = LocalCostSupplier.objects.create(rule=rule_,
                                                     supplier_price_higher_check=True)
            rule_.cost = local_cost_price
            rule_.cost_unit = local_cost_price_unit
            rule_.price_dependancey = local_cost_price_competitor
            rule_.percentage = local_cost_price_percentage
            rule_.percentage_unit = local_cost_price_percentage_unit

            if local_cost_supplier == 0:
                rule_.supplier.add(*[x for x in Suppliers.objects.all()])
                rule_.is_all_suppliers = True
            else:
                supplier_ = Suppliers.objects.get(id=local_cost_supplier)
                rule_.supplier.add(supplier_)
                rule_.is_all_suppliers = False

            if local_cost_category:
                rule_.is_on_category = True
                if 0 in local_cost_category:
                    rule_.category.add(*[x for x in Categories.objects.all()])
                    rule_.is_all_categories = True
                else:
                    rule_.category.add(*[Categories.objects.get(id=int(x)) for x in local_cost_category])
                    rule_.is_all_categories = False
            else:
                pro_ = Products.objects.get(sku=local_cost_product_sku)
                rule_.product_sku = pro_
                rule_.is_on_category = False
            rule_.save()
        else:
            lcp.cost = local_cost_price
            lcp.price_dependancey = local_cost_price_competitor
            lcp.cost_unit = local_cost_price_unit
            lcp.percentage_unit = local_cost_price_percentage_unit
            lcp.percentage = local_cost_price_percentage
            lcp.save()

    def add_thenx_cost_supplier_rule(self):
        thenx_cost_price = self.request['thenx_cost_price']
        thenx_cost_price_competitor = self.request['thenx_cost_price_competitor']
        thenx_cost_price_percentage = self.request['thenx_cost_price_percentage']
        thenx_cost_supplier = int(self.request['thenx_cost_supplier'])
        thenx_cost_category = self.request['thenx_cost_category']
        thenx_cost_product_sku = self.request['thenx_cost_product_sku']
        thenx_cost_price_unit = self.request['thenx_cost_price_unit']
        thenx_cost_price_percentage_unit = self.request['thenx_cost_price_percentage_unit']

        is_supplier_exists = False
        is_category_info = False
        is_all_categories = False

        if thenx_cost_category:
            thenx_cost_category = [int(x) for x in thenx_cost_category.split(',')]
            is_category_info = True
            if 0 in thenx_cost_category:
                is_all_categories = True

        if thenx_cost_product_sku:
            product_ = Products.objects.filter(sku=thenx_cost_product_sku).last()
            if not product_:
                return

        # Rules validation to stop duplication
        if thenx_cost_supplier != 0 and is_category_info == True and is_all_categories == True:
            if ThenxCostSupplier.objects.filter(is_all_suppliers=False, supplier__reference_id=thenx_cost_supplier,
                                                is_all_categories=True).exists():
                is_supplier_exists = True
                tcp = ThenxCostSupplier.objects.filter(is_all_suppliers=False,
                                                       supplier__reference_id=thenx_cost_supplier,
                                                       is_all_categories=True).last()

        if thenx_cost_supplier != 0 and is_category_info == False:
            if ThenxCostSupplier.objects.filter(is_all_suppliers=False, supplier__reference_id=thenx_cost_supplier,
                                                is_on_category=False,
                                                product_sku__sku=thenx_cost_product_sku).exists():
                is_supplier_exists = True
                tcp = ThenxCostSupplier.objects.filter(is_all_suppliers=False,
                                                       supplier__reference_id=thenx_cost_supplier,
                                                       is_on_category=False,
                                                       product_sku__sku=thenx_cost_product_sku).last()

        if thenx_cost_supplier == 0 and is_category_info == True and is_all_categories == True:
            if ThenxCostSupplier.objects.filter(is_all_suppliers=True, is_all_categories=True).exists():
                is_supplier_exists = True
                tcp = ThenxCostSupplier.objects.filter(is_all_suppliers=True, is_all_categories=True).last()

        if thenx_cost_supplier == 0 and is_category_info == False:
            if ThenxCostSupplier.objects.filter(is_all_suppliers=True, product_sku__sku=thenx_cost_product_sku,
                                                is_on_category=False).exists():
                is_supplier_exists = True
                tcp = ThenxCostSupplier.objects.filter(is_all_suppliers=True,
                                                       is_on_category=False,
                                                       product_sku__sku=thenx_cost_product_sku).last()

        if not is_supplier_exists:
            rule_ = Rules.objects.create(rule_type=5)
            rule_ = ThenxCostSupplier.objects.create(rule=rule_, supplier_price_higher_check=True)
            rule_.cost = thenx_cost_price
            rule_.price_dependancey = thenx_cost_price_competitor
            rule_.percentage = thenx_cost_price_percentage
            rule_.percentage_unit = thenx_cost_price_percentage_unit
            rule_.cost_unit = thenx_cost_price_unit
            rule_.save()

            if thenx_cost_supplier == 0:
                rule_.supplier.add(*[x for x in Suppliers.objects.all()])
                rule_.is_all_suppliers = True
            else:
                supplier_ = Suppliers.objects.get(id=thenx_cost_supplier)
                rule_.supplier.add(supplier_)
                rule_.is_all_suppliers = False

            if thenx_cost_category:
                rule_.is_on_category = True
                if 0 in thenx_cost_category:
                    rule_.category.add(*[x for x in Categories.objects.all()])
                    rule_.is_all_categories = True
                else:
                    rule_.category.add(*[Categories.objects.get(id=int(x)) for x in thenx_cost_category])
                    rule_.is_all_categories = False
            else:
                pro_ = Products.objects.get(sku=thenx_cost_product_sku)
                rule_.product_sku = pro_
                rule_.is_on_category = False
            rule_.save()
        else:
            tcp.percentage_unit = thenx_cost_price_percentage_unit
            tcp.cost_unit = thenx_cost_price_unit
            tcp.cost = thenx_cost_price
            tcp.price_dependancey = thenx_cost_price_competitor
            tcp.percentage = thenx_cost_price_percentage
            tcp.save()
