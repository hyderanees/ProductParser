# Generated by Django 2.2 on 2020-11-15 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_adminlogofjobtoshow_is_competitor_asscoiated'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminlogofjobtoshow',
            name='is_competitor_less_than_cost',
            field=models.BooleanField(default=False),
        ),
    ]
