# Generated by Django 2.2.24 on 2021-09-06 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0144_auto_20210905_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='sms_attempts',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sms_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sms_date',
        ),
    ]
