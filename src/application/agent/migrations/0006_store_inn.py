# Generated by Django 2.1 on 2018-11-17 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0005_order_ordergood'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='inn',
            field=models.CharField(blank=True, default='', max_length=12, verbose_name='Inn'),
        ),
    ]
