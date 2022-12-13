# Generated by Django 2.1 on 2019-12-23 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0056_auto_20191222_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetask',
            name='add_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Add value'),
        ),
        migrations.AddField(
            model_name='storetask',
            name='is_add_value',
            field=models.BooleanField(blank=True, default=False, verbose_name='Is add value'),
        ),
    ]
