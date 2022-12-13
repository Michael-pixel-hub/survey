# Generated by Django 2.2.24 on 2022-02-11 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0021_auto_20220211_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='box_count',
            field=models.IntegerField(blank=True, default=1, verbose_name='Кол-во в коробке'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='price',
            field=models.FloatField(blank=True, default=0, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='box_count',
            field=models.IntegerField(default=1, verbose_name='Кол-во в коробке'),
        ),
        migrations.AlterField(
            model_name='product',
            name='min_count',
            field=models.IntegerField(default=1, verbose_name='Минимальное количество'),
        ),
    ]