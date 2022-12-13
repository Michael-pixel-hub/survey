# Generated by Django 2.1 on 2019-02-18 18:54

import application.survey.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0017_user_is_need_solar_staff_reg'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='api_key',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='API key'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_telegram',
        ),
        migrations.AddField(
            model_name='user',
            name='source',
            field=models.CharField(db_index=True, default='Telegram', max_length=100, verbose_name='Source'),
        ),
    ]
