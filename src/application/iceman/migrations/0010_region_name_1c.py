# Generated by Django 2.2.24 on 2022-01-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0009_region_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='name_1c',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Name'),
        ),
    ]
