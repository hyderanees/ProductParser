# Generated by Django 2.2 on 2021-01-03 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_productcompetitorsitesreference_error_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='cost_unit',
            field=models.IntegerField(default=0),
        ),
    ]
