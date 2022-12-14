# Generated by Django 2.2.24 on 2022-04-15 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0085_auto_20220415_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='online_payment',
        ),
        migrations.AlterField(
            model_name='source',
            name='discount',
            field=models.FloatField(blank=True, default=5, help_text='Процент скидки при выборе оплаты по факту. 0 - нет скидки.', verbose_name='Скидка оплаты по факту в %'),
        ),
    ]
