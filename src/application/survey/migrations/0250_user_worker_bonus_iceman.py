# Generated by Django 2.2.28 on 2022-11-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0249_auto_20221108_1217'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='worker_bonus_iceman',
            field=models.FloatField(blank=True, help_text='Какой % от стоимости товара выплачивается торговому представителю.', null=True, verbose_name='Бонус в % для работника'),
        ),
    ]
