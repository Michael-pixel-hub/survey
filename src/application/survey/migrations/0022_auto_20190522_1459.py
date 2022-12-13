# Generated by Django 2.1 on 2019-05-22 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0021_auto_20190516_1120'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='static_latitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='user',
            name='static_longitude',
            field=models.FloatField(blank=True, null=True, verbose_name='Longitude'),
        ),
    ]