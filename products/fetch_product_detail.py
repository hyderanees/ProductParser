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


class FetchProductDetail:

    def __init__(self, pc_query_set):
        self.product_competitors_query_set = pc_query_set
        self.response_list = []

    def iterate_over_query_set(self):
        for obj in self.product_competitors_query_set:
            if obj.site_reference.reference_id == 1:
                self.get_detail_of_distrizone(obj.link)
            if obj.site_reference.reference_id == 2:
                self.get_detail_of_gsmnet(obj.link)
            if obj.site_reference.reference_id == 3:
                self.get_detail_of_inowgsm(obj.link)
            if obj.site_reference.reference_id == 4:
                self.get_detail_of_magazingsm(obj.link)
            if obj.site_reference.reference_id == 5:
                self.get_detail_of_mokagsm(obj.link)
            if obj.site_reference.reference_id == 6:
                self.get_detail_of_powerlaptop(obj.link)
            if obj.site_reference.reference_id == 7:
                self.get_detail_of_protableta(obj.link)
            if obj.site_reference.reference_id == 8:
                self.get_detail_of_servicepack(obj.link)
            if obj.site_reference.reference_id == 9:
                self.get_detail_of_sepmobile(obj.link)
            if obj.site_reference.reference_id == 10:
                self.get_detail_of_sunnex_mobile(obj.link)
            if obj.site_reference.reference_id == 12:
                self.get_detail_of_tradegsm_mobile(obj.link)

    def get_detail_of_distrizone(self, url):
        try:
            self.response_list.append(DistriZoneInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_gsmnet(self, url):
        try:
            self.response_list.append(GSMNETInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_inowgsm(self, url):
        try:
            self.response_list.append(InowGSMInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_magazingsm(self, url):
        try:
            self.response_list.append(MagaZingSMInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_mokagsm(self, url):
        try:
            self.response_list.append(MokaGSMInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_powerlaptop(self, url):
        try:
            self.response_list.append(PowerLaptopInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_protableta(self, url):
        try:
            self.response_list.append(ProtabletaInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_servicepack(self, url):
        try:
            self.response_list.append(ServicePackInformation(url).get_prices())
        except Exception as e:
            print (e)

    def get_detail_of_sepmobile(self, url):
        try:
            response___ = SEPMobileMainFunction(url)
            if response___:
                self.response_list.append(response___)
        except Exception as e:
            print (e)

    def get_detail_of_sunnex_mobile(self, url):
        try:
            response___ = SunnexMobile(url)
            if response___:
                self.response_list.append(response___)
        except Exception as e:
            print (e)

    def get_detail_of_tradegsm_mobile(self, url):
        try:
            response___ = TradeGSMInformation(url).get_prices()
            if response___:
                self.response_list.append(response___)
        except Exception as e:
            print (e)

    def return_final_response(self):
        return self.response_list
