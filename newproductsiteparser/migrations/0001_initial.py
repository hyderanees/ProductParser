# Generated by Django 2.2 on 2021-07-24 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MagazingGsmExistingProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='')),
                ('price', models.TextField(default='')),
                ('promotional_price', models.TextField(default='')),
                ('href_link', models.TextField(default='')),
                ('img_tag', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
