from background_task import background
from .product_fetching_job import product_fetching_jobs
from .product_competitor_links_from_server import product_competitor_fetching_job_from_server
from .models import InstantJobDeclaration
from .product_competitor_background_job import product_competitor_job


@background(queue='upload-file-queue')
def start_product_and_other_detail_fetching(ijd):
    print('start dealing with new product start')
    try:
        product_fetching_jobs()
    except Exception as e:
        print(e)
    InstantJobDeclaration.objects.filter(id=ijd).update(status=1)


@background(queue='upload-file-queue')
def start_product_competitor_fetching(ijd):
    print('start dealing with new product competitor start')
    try:
        product_competitor_fetching_job_from_server()
    except Exception as e:
        print(e)
    InstantJobDeclaration.objects.filter(id=ijd).update(status=1)


@background(queue='upload-file-queue')
def start_product_competitor_job(ijd):
    print('start competitors only bro')
    product_competitor_job(ijd)
