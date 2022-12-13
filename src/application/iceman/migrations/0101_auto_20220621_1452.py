# Generated by Django 2.2.24 on 2022-06-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0100_order_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Новый'), (2, 'Просрочен'), (3, 'Оплачен'), (4, 'Отменен'), (5, 'Модерация')], default=1, verbose_name='Статус'),
        ),
    ]
