# Generated by Django 2.2.20 on 2021-06-26 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0085_assortment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadrequests',
            name='request_data_type',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Request data type'),
        ),
    ]
