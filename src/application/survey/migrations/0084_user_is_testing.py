# Generated by Django 2.2.20 on 2021-06-21 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0083_auto_20210617_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_testing',
            field=models.BooleanField(default=False, verbose_name='Testing mode'),
        ),
    ]