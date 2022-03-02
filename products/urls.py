from django.conf.urls.static import static
from django.urls import path

from productparser.settings import MEDIA_ROOT, MEDIA_URL
from .views import *
from .weekly_new_product_report import get_new_product_details
from .newDesignViews import *


app_name = 'products'
urlpatterns = [
                  path('home', home, name='home'),

                  path('scrapping_job_links', scrapping_job_links, name='scrapping_job_links'),
                  path('delete_scrapping_links', delete_scrapping_links, name='delete_scrapping_links'),

                  path('products', products, name='products'),

                  path('products_new', products_new, name='products_new'),
                  path('competitors_info_new', competitors_info_new, name='competitors_info_new'),

                  path('products/upload_products', upload_products, name='upload_products'),
                  path('delete_products_info', delete_products_info, name='delete_products_info'),
                  path('update_products_smart_price_info', update_products_smart_price_info,
                       name='update_products_smart_price_info'),
                  path('products/upload_product_competitors', upload_product_competitors,
                       name='upload_product_competitors'),

                  # Product Details
                  path('products/detail/<int:product_id>/', product_detail, name='product_detail'),
                  path('add_product_competitor', add_product_competitor, name='add_product_competitor'),
                  path('delete_product_competitor', delete_product_competitor, name='delete_product_competitor'),
                  path('fetch_product_details', fetch_product_details, name='fetch_product_details'),
                  path('fetch_testing_info', fetch_testing_info, name='fetch_testing_info'),

                  path('categories', categories, name='categories'),
                  path('brands', brands, name='brands'),
                  path('suppliers', suppliers, name='suppliers'),
                  path('rules/add', add_rules, name='add_rules'),
                  path('add_rules_csv', add_rules_csv, name='add_rules_csv'),
                  path('edit_rule', edit_rule, name='edit_rule'),
                  path('get_rule_detail', get_rule_detail, name='get_rule_detail'),
                  path('rules', rules, name='rules'),
                  path('delete_rule', delete_rule, name='delete_rule'),
                  path('delete_all_rule', delete_all_rule, name='delete_all_rule'),
                  path('filter_costs_viewer', filter_costs_viewer, name='filter_costs_viewer'),
                  path('products_sku', products_sku, name='products_sku'),

                  path('new_product_details', get_new_product_details, name='get_new_product_details'),

                  path('daily_update', daily_update, name='daily_update'),
                  path('instant_push', instant_push, name='instant_push'),
                  path('register_push_event', register_push_event, name='register_push_event'),
                  path('register_products_job', register_products_job, name='register_products_job'),
                  path('register_product_competitor_job', register_product_competitor_job,
                       name='register_product_competitor_job'),
                  path('update_all_daily_report', update_all_daily_report, name='update_all_daily_report'),
                  path('update_smart_price', update_smart_price, name='update_smart_price'),
                  path('update_smart_price_of_product', update_smart_price_of_product, name='update_smart_price_of_product'),

                  path('competitors_info', competitors_info, name='competitors_info'),
                  path('competitors_info/all_competitors_info', all_competitors_info, name='all_competitors_info'),
                  path('updated_on_thenx', updated_on_thenx, name='updated_on_thenx'),
                  path('delete_competitor_info', delete_competitor_info, name='delete_competitor_info'),
                  path('update_competitor_info', update_competitor_info, name='update_competitor_info'),
                  path('update_all_competitor_info', update_all_competitor_info, name='update_all_competitor_info'),
                  path('send_email', send_email, name='send_email'),
                  path('download_csv_file', download_csv_file, name='download_csv_file'),
                  path('export_csv_file', export_csv_file, name='export_csv_file'),
                  path('export_products_csv_file', export_products_csv_file, name='export_products_csv_file'),
                  path('export_scraping_csv_file', export_scraping_csv_file, name='export_scraping_csv_file'),

                  # dump information
                  path('dump_categories_job', dump_categories_job, name='dump_categories_job'),
                  path('dump_brands_job', dump_brands_job, name='dump_brands_job'),
                  path('dump_suppliers_job', dump_suppliers_job, name='dump_suppliers_job'),
                  path('dump_competitors_info_job', dump_competitors_info_job, name='dump_competitors_info_job'),
                  path('dump_products_info', dump_products_info, name='dump_products_info'),

                  # cron logs
                  path('job_logs', job_logs, name='job_logs'),
                  path('job_detail', job_detail, name='job_detail'),
                  path('delete_all_data', delete_all_data, name='delete_all_data'),
                  path('delete_competitors_data', delete_competitors_data, name='delete_competitors_data'),

                  path('users_info', users_info, name='users_info'),
                  path('reset_password', reset_password, name='reset_password'),
                  path('delete_user', delete_user, name='delete_user'),
                  path('update_permission_of_user', update_permission_of_user, name='update_permission_of_user'),
                  path('add_new_user', add_new_user, name='add_new_user'),

                  # product fetching jobs
                  path('test_product_scrapping', test_product_scrapping, name='test_product_scrapping'),
                  path('test_product_cron', test_product_cron, name='test_product_cron'),
                  path('test_product_fetching_items', test_product_fetching_items, name='test_product_fetching_items'),
                  path('test_email_csv_files', test_email_csv_files, name='test_email_csv_files'),
                  path('test_product_competitor_link', test_product_competitor_link, name='test_product_competitor_link'),

              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)
