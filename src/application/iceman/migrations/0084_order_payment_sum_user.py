# Generated by Django 2.2.24 on 2022-04-15 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0083_auto_20220415_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_sum_user',
            field=models.FloatField(blank=True, default=0, verbose_name='Сумма выплаты пользователю'),
        ),
    ]