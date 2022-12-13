# Generated by Django 2.2.24 on 2022-02-23 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0041_auto_20220222_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(default='', max_length=15, verbose_name='Штрихкод'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(blank=True, null=True, verbose_name='Вес в граммах'),
        ),
    ]
