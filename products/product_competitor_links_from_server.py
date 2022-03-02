from products.models import *
from products.utils import get_competitor_links_from_server, upload_competitor_info_against_product


def product_competitor_fetching_job_from_server():
    cron_ = CronJobLogRunning.objects.create(cron_job_type=2)
    response_list = get_competitor_links_from_server()
    new_pro = upload_competitor_info_against_product(response_list)

    cron_.scanned_sku = len(response_list)
    cron_.new_sku = new_pro
    cron_.changed_prices = 0
    cron_.save()
