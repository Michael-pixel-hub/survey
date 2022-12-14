# Generated by Django 2.2.16 on 2020-10-21 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0047_order_from_1c_cashback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'New'), (2, 'Payed'), (3, 'Pay in Solar'), (6, 'Payed cashback'), (4, 'Canceled'), (5, 'Finished')], default=1, verbose_name='Status'),
        ),
    ]
