# Generated by Django 2.2.28 on 2022-08-26 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0107_store_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_courier',
            field=models.FloatField(blank=True, null=True, verbose_name='Деньги водителю'),
        ),
    ]
