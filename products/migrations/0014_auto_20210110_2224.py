# Generated by Django 2.2 on 2021-01-10 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_products_cost_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='marginrules',
            name='higher_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='marginrules',
            name='higher_percentage_unit',
            field=models.IntegerField(default=2),
        ),
    ]