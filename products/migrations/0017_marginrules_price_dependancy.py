# Generated by Django 2.2 on 2021-01-17 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20210118_0010'),
    ]

    operations = [
        migrations.AddField(
            model_name='marginrules',
            name='price_dependancy',
            field=models.FloatField(default=0),
        ),
    ]
