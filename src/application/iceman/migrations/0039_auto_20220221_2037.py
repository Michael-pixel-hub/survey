# Generated by Django 2.2.24 on 2022-02-21 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0038_remove_stock_source'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sourceproduct',
            options={'ordering': ['source__name', 'order'], 'verbose_name': 'Товар в магазине', 'verbose_name_plural': 'Товары в магазинах'},
        ),
    ]
