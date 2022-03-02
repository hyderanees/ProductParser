from django import template
from products.models import UsersPermissions

register = template.Library()


@register.filter
def check_home_page_permission(user):
    if UsersPermissions.objects.filter(user=user, is_home_page=True).exists():
        return True
    return False


@register.filter(name='has_group')
def has_group(user, group_name):
    if user.is_superuser:
        return True
    if group_name == 'products':
        return UsersPermissions.objects.filter(user=user, is_products_page=True).exists()
    if group_name == 'rules':
        return UsersPermissions.objects.filter(user=user, is_rules_page=True).exists()
    if group_name == 'competitors':
        return UsersPermissions.objects.filter(user=user, is_competitors_page=True).exists()
    if group_name == 'dailyprice':
        return UsersPermissions.objects.filter(user=user, is_daily_price_page=True).exists()
    if group_name == 'activelinks':
        return UsersPermissions.objects.filter(user=user, is_active_links_page=True).exists()
    if group_name == 'cronlogs':
        return UsersPermissions.objects.filter(user=user, is_cron_job_logs_page=True).exists()
    return False
