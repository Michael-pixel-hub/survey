# Generated by Django 2.2.24 on 2022-04-15 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0089_auto_20220415_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='payment_days',
            field=models.IntegerField(blank=True, default=10, verbose_name='Кол-во дней отсрочки'),
        ),
    ]
