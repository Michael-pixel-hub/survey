# Generated by Django 2.2.24 on 2022-04-15 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0084_order_payment_sum_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_sum_user',
            field=models.FloatField(blank=True, default=0, verbose_name='Выплата пользователю'),
        ),
    ]