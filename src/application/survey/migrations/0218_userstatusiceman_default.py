# Generated by Django 2.2.24 on 2022-06-26 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0217_auto_20220625_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstatusiceman',
            name='default',
            field=models.BooleanField(default=False, verbose_name='По умолчанию'),
        ),
    ]
