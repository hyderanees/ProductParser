from django.db import models


class MagazingGsmExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class ServicePackExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class MokaGsmExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class PortabletaExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class DistrizoneExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class GsmnetExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class SunnexExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)


class SepMobileExistingProducts(models.Model):
    title = models.TextField(default='')
    price = models.TextField(default='')
    promotional_price = models.TextField(default='')
    href_link = models.TextField(default='')
    img_tag = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

