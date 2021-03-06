# Generated by Django 2.2 on 2020-11-23 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20201122_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminlogofjobtoshow',
            name='same_moment_calculated_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='products',
            name='is_smart_price_already_set',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='products',
            name='smart_price_value',
            field=models.FloatField(default=0.0),
        ),
    ]
