# Generated by Django 2.2 on 2020-11-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_adminlogofjobtoshow_is_smart_price_set_applied'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcompetitorsitesreference',
            name='error_information',
            field=models.TextField(default=''),
        ),
    ]
