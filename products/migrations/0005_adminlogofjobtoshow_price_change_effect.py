# Generated by Django 2.2 on 2020-11-14 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20201114_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminlogofjobtoshow',
            name='price_change_effect',
            field=models.IntegerField(default=0),
        ),
    ]
