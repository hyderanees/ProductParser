from django.urls import path
from .views import *

urlpatterns = [
    # path('magazing-gsm-test', test_magazin_gsm_information),
    # path('service-pack-test', test_service_pack_information),
    # path('moka-gsm-test', test_moka_gsm_information),
    # path('distrizone-test', test_distrizone_information),
    # path('gsmnet-test', test_gsmnet_information),
    path('sunnex-test', test_sunnex_information),
    path('sepmobile-test', test_sepmobile_information),
    path('cron-data-test', test_cron_fetching_new_product),
]
