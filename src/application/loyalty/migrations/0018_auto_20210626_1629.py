# Generated by Django 2.2.20 on 2021-06-26 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0017_store_price_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='price_type',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Price type'),
        ),
    ]
