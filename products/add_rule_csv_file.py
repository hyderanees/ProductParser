from .models import *
import io
import csv


class AddCSVRule:
    def __init__(self, request):
        self.csv_file = request.FILES['file']
        self.data_set = self.get_data_set_values()

    @staticmethod
    def get_margin_price_unit(col):
        if col.lower().strip() == 'percentage' or col.lower().strip() == 'percent':
            return 2
        else:
            return 1

    @staticmethod
    def get_supplier(col):
        if col.lower().strip() == 'all':
            return 0
        else:
            supplier_ = Suppliers.objects.filter(name__iexact=col.strip()).last()
            if supplier_:
                return supplier_.id
            return 0

    def get_data_set_values(self):
        data_set = self.csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        return io_string

    def dump_margin_rule(self):
        def get_margin_type(col):
            if col.lower() == 'retail':
                return 1
            else:
                return 0

        for column in csv.reader(self.data_set, delimiter=','):
            try:
                margin_type = get_margin_type(column[0])
                margin_price_unit = self.get_margin_price_unit(column[2])
                margin_price = float(column[1])
                margin_supplier = self.get_supplier(column[3])
                margin_category = column[4]
                margin_product_sku = column[5]
                price_dependancy = column[6]
                price_dependancy2 = column[7]
                lower_price = float(column[8])
                lower_price_unit = self.get_margin_price_unit(column[9])
                higher_price = float(column[10])
                higher_price_unit = self.get_margin_price_unit(column[11])

                if margin_type and margin_price and margin_price_unit:
                    self.add_margin_rule(margin_type, margin_price, margin_price_unit, margin_supplier, margin_category,
                                         margin_product_sku, price_dependancy,price_dependancy2, lower_price, lower_price_unit,
                                         higher_price, higher_price_unit)
            except Exception as e:
                print(e)

    @staticmethod
    def add_margin_rule(margin_type, margin_price, margin_price_unit, margin_supplier, margin_category,
                        margin_product_sku, price_dependancy, price_dependancy2, lower_price, lower_price_unit, higher_price,
                        higher_price_unit):
        # margin_type = int(self.request['margin_type']) if 'margin_type' in self.request else 0
        # margin_price = self.request['margin_price'] if 'margin_price' in self.request else 0
        # margin_supplier = int(self.request['margin_supplier']) if 'margin_supplier' in self.request else 0
        # margin_price_unit = int(self.request['margin_price_unit']) if 'margin_price_unit' in self.request else 0
        # margin_category = self.request['margin_category'] if 'margin_category' in self.request else ''
        # margin_product_sku = self.request['margin_product_sku'] if 'margin_product_sku' in self.request else ''

        is_category_info = False
        is_all_categories = False
        is_supplier_exists = False

        if margin_category:
            if margin_category.lower().strip() == 'all':
                is_all_categories = True

            mc__ = Categories.objects.filter(name__iexact=margin_category.strip()).last()
            if mc__:
                margin_category = [mc__.id]
            else:
                margin_category = []

            if is_all_categories:
                margin_category.append(0)

            is_category_info = True

        if margin_product_sku:
            product_ = Products.objects.filter(sku=margin_product_sku.strip()).last()
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
                                               percentage_unit=margin_price_unit, price_dependancy=price_dependancy,
                                               price_dependancy2=price_dependancy2,
                                               lower_percentage=lower_price, lower_percentage_unit=lower_price_unit,
                                               higher_percentage=higher_price, higher_percentage_unit=higher_price_unit)

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
            mr.percentage_unit = margin_price_unit
            mr.price_dependancy = price_dependancy
            mr.price_dependancy2 = price_dependancy2
            mr.lower_percentage = lower_price
            mr.lower_percentage_unit = lower_price_unit
            mr.higher_percentage = higher_price
            mr.higher_percentage_unit = higher_price_unit
            mr.save()

    def dump_local_cost_rule(self):

        for column in csv.reader(self.data_set, delimiter=','):
            try:
                local_cost_price = float(column[0])
                local_cost_price_unit = self.get_margin_price_unit(column[1])
                local_cost_price_competitor = float(column[2])
                local_cost_price_percentage = float(column[3])
                local_cost_price_percentage_unit = self.get_margin_price_unit(column[4])
                local_cost_supplier = self.get_supplier(column[5])
                local_cost_category = column[6]
                local_cost_product_sku = column[7]

                if local_cost_price and local_cost_price_unit and local_cost_price_competitor and \
                        local_cost_price_percentage \
                        and local_cost_price_percentage_unit:
                    self.add_local_cost_supplier_rule(local_cost_price, local_cost_price_unit,
                                                      local_cost_price_competitor,
                                                      local_cost_price_percentage, local_cost_price_percentage_unit,
                                                      local_cost_supplier, local_cost_category, local_cost_product_sku)
            except Exception as e:
                print(e)

    @staticmethod
    def add_local_cost_supplier_rule(local_cost_price, local_cost_price_unit, local_cost_price_competitor,
                                     local_cost_price_percentage, local_cost_price_percentage_unit,
                                     local_cost_supplier, local_cost_category, local_cost_product_sku):

        is_supplier_exists = False
        is_category_info = False
        is_all_categories = False

        if local_cost_category:
            if local_cost_category.lower().strip() == 'all':
                is_all_categories = True

            mc__ = Categories.objects.filter(name__iexact=local_cost_category.strip()).last()
            if mc__:
                local_cost_category = [mc__.id]
            else:
                local_cost_category = []

            if is_all_categories:
                local_cost_category.append(0)

            is_category_info = True

        if local_cost_product_sku:
            product_ = Products.objects.filter(sku=local_cost_product_sku.strip()).last()
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

    def dump_thenx_cost_rule(self):
        for column in csv.reader(self.data_set, delimiter=','):
            try:
                thenx_cost_price = float(column[0])
                thenx_cost_price_unit = self.get_margin_price_unit(column[1])
                thenx_cost_price_competitor = float(column[2])
                thenx_cost_price_percentage = float(column[3])
                thenx_cost_price_percentage_unit = self.get_margin_price_unit(column[4])
                thenx_cost_supplier = self.get_supplier(column[5])
                thenx_cost_category = column[6]
                thenx_cost_product_sku = column[7]

                if thenx_cost_price and thenx_cost_price_unit and thenx_cost_price_competitor and thenx_cost_price_percentage \
                        and thenx_cost_price_percentage_unit:
                    self.add_thenx_cost_supplier_rule(thenx_cost_price, thenx_cost_price_unit,
                                                      thenx_cost_price_competitor,
                                                      thenx_cost_price_percentage, thenx_cost_price_percentage_unit,
                                                      thenx_cost_supplier, thenx_cost_category, thenx_cost_product_sku)
            except Exception as e:
                print(e)

    @staticmethod
    def add_thenx_cost_supplier_rule(thenx_cost_price, thenx_cost_price_unit, thenx_cost_price_competitor,
                                     thenx_cost_price_percentage, thenx_cost_price_percentage_unit,
                                     thenx_cost_supplier, thenx_cost_category, thenx_cost_product_sku):

        is_supplier_exists = False
        is_category_info = False
        is_all_categories = False

        if thenx_cost_category:
            if thenx_cost_category.lower().strip() == 'all':
                is_all_categories = True
            mc__ = Categories.objects.filter(name__iexact=thenx_cost_category.strip()).last()
            if mc__:
                thenx_cost_category = [mc__.id]
            else:
                thenx_cost_category = []
            is_category_info = True

            if is_all_categories:
                thenx_cost_category.append(0)

        if thenx_cost_product_sku:
            product_ = Products.objects.filter(sku=thenx_cost_product_sku.strip()).last()
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
