# Generated by Django 2.2.28 on 2022-09-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0111_auto_20220904_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storetask',
            name='day_of_week',
        ),
        migrations.AddField(
            model_name='storetask',
            name='days_of_week',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='Days of weeks'),
        ),
    ]
