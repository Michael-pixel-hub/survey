# Generated by Django 2.2.28 on 2022-05-04 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0098_auto_20220504_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_sum_user',
            field=models.FloatField(blank=True, default=0, verbose_name='Бонус'),
        ),
    ]