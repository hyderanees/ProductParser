from .utils import *


class RulesFilter:

    def __init__(self, request):
        self.is_all_categories = False
        self.is_all_suppliers = False
        self.request = request
        self.data = self.request.POST
        self.category = self.data['category']
        self.supplier = self.data['supplier']
        self.product = self.data['product']
        self.is_lcp = self.data['islcp']
        self.check_all_values()

    def check_all_values(self):
        if self.supplier:
            if int(self.supplier) == 0:
                self.is_all_suppliers = True
        if self.category:
            if int(self.category) == 0:
                self.is_all_categories = True

    def get_response(self):
        if int(self.is_lcp) == 1:
            return self.get_response_of_lcp()
        elif int(self.is_lcp) == 0:
            return self.get_response_of_tcs()
        elif int(self.is_lcp) == 2:
            return self.get_response_of_margin()
        elif int(self.is_lcp) == 3:
            return self.get_response_of_competitor()

    def get_response_of_lcp(self):
        lcp = []
        if self.is_all_suppliers and self.is_all_categories:
            lcp = LocalCostSupplier.objects.filter(is_all_suppliers=self.is_all_suppliers,
                                                   is_all_categories=self.is_all_categories)
        elif self.is_all_suppliers:
            lcp = LocalCostSupplier.objects.filter(is_all_suppliers=self.is_all_suppliers)
        elif self.is_all_categories:
            lcp = LocalCostSupplier.objects.filter(is_all_categories=self.is_all_categories)
        else:
            # if self.category or self.product or self.supplier:
            lcp = LocalCostSupplier.objects.all()

        if self.category != '0' and self.category:
            lcp = lcp.filter(category__id=int(self.category))
        if self.supplier != '0' and self.supplier:
            lcp = lcp.filter(supplier__id=int(self.supplier))
        if self.product != 'product' and self.product:
            lcp = lcp.filter(product_sku__sku=int(self.product))

        lcp = [get_local_cost_supplier(x.rule) for x in lcp]

        return lcp

    def get_response_of_tcs(self):
        tcs = []
        if self.is_all_suppliers and self.is_all_categories:
            tcs = ThenxCostSupplier.objects.filter(is_all_suppliers=self.is_all_suppliers,
                                                   is_all_categories=self.is_all_categories)
        elif self.is_all_suppliers:
            tcs = ThenxCostSupplier.objects.filter(is_all_suppliers=self.is_all_suppliers)
        elif self.is_all_categories:
            tcs = ThenxCostSupplier.objects.filter(is_all_categories=self.is_all_categories)
        else:
            # if self.category or self.product or self.supplier:
            tcs = ThenxCostSupplier.objects.all()

        if self.category != '0' and self.category:
            tcs = tcs.filter(category__id=int(self.category))
        if self.supplier != '0' and self.supplier:
            tcs = tcs.filter(supplier__id=int(self.supplier))
        if self.product != 'product' and self.product:
            tcs = tcs.filter(product_sku__sku=int(self.product))

        tcs = [get_thenx_cost_supplier(x.rule) for x in tcs]

        return tcs

    def get_response_of_margin(self):
        margin_rules = []
        if self.is_all_suppliers and self.is_all_categories:
            margin_rules = MarginRules.objects.filter(is_all_suppliers=self.is_all_suppliers,
                                                      is_all_categories=self.is_all_categories)
        elif self.is_all_suppliers:
            margin_rules = MarginRules.objects.filter(is_all_suppliers=self.is_all_suppliers)
        elif self.is_all_categories:
            margin_rules = MarginRules.objects.filter(is_all_categories=self.is_all_categories)
        else:
            # if self.category or self.product or self.supplier:
            margin_rules = MarginRules.objects.all()

        if self.category != '0' and self.category:
            margin_rules = margin_rules.filter(category__id=int(self.category))
        if self.supplier != '0' and self.supplier:
            margin_rules = margin_rules.filter(supplier__id=int(self.supplier))
        if self.product != 'product' and self.product:
            margin_rules = margin_rules.filter(product_sku__sku=int(self.product))

        margin_rules = [get_margin_rule(x.rule) for x in margin_rules]

        return margin_rules

    def get_response_of_competitor(self):
        competitor = []
        if self.is_all_suppliers and self.is_all_categories:
            competitor = PriceCompetitorRule.objects.filter(is_all_suppliers=self.is_all_suppliers,
                                                   is_all_categories=self.is_all_categories)
        elif self.is_all_suppliers:
            competitor = PriceCompetitorRule.objects.filter(is_all_suppliers=self.is_all_suppliers)
        elif self.is_all_categories:
            competitor = PriceCompetitorRule.objects.filter(is_all_categories=self.is_all_categories)
        else:
            # if self.category or self.product or self.supplier:
            competitor = PriceCompetitorRule.objects.all()

        if self.category != '0' and self.category:
            competitor = competitor.filter(category__id=int(self.category))
        if self.supplier != '0' and self.supplier:
            competitor = competitor.filter(supplier__id=int(self.supplier))
        if self.product != 'product' and self.product:
            competitor = competitor.filter(product_sku__sku=int(self.product))

        competitor = [get_competitor_rule(x.rule) for x in competitor]

        return competitor