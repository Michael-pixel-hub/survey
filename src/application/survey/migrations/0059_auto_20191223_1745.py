# Generated by Django 2.1 on 2019-12-23 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0058_auto_20191223_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='remove_days',
            field=models.IntegerField(blank=True, null=True, verbose_name='Remove days'),
        ),
        migrations.AddField(
            model_name='task',
            name='remove_money',
            field=models.FloatField(blank=True, null=True, verbose_name='Remove sum'),
        ),
        migrations.AddField(
            model_name='task',
            name='remove_ppl',
            field=models.IntegerField(blank=True, null=True, verbose_name='Remove ppl'),
        ),
    ]
