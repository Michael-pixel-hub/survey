# Generated by Django 2.2.24 on 2022-02-12 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0027_auto_20220212_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='online_payment_sum',
            field=models.FloatField(blank=True, default=0, verbose_name='Сумма платежа'),
        ),
    ]
