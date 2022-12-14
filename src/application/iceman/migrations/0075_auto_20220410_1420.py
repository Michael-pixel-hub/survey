# Generated by Django 2.2.24 on 2022-04-10 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0074_auto_20220408_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('cash', 'Наличными'), ('account', 'Безналичный'), ('delay', 'Отсрочка')], max_length=20, null=True, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('online', 'Онлайн'), ('delay', 'Отсрочка')], max_length=20, null=True, verbose_name='Срок оплаты'),
        ),
    ]
