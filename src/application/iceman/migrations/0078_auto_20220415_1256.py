# Generated by Django 2.2.24 on 2022-04-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0077_auto_20220414_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('entity', 'Юридическое лицо'), ('individual', 'Физическое лицо')], default='entity', max_length=20, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('delay', 'Отсрочка'), ('fact', 'Факт')], default='delay', max_length=20, verbose_name='Тип оплаты'),
        ),
    ]
