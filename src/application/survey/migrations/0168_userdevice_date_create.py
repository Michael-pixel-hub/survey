# Generated by Django 2.2.24 on 2021-11-30 13:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0167_auto_20211130_0423'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdevice',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date create'),
            preserve_default=False,
        ),
    ]