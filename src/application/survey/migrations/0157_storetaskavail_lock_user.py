# Generated by Django 2.2.24 on 2021-09-14 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0156_auto_20210914_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetaskavail',
            name='lock_user',
            field=models.IntegerField(blank=True, null=True, verbose_name='Lock user id'),
        ),
    ]
