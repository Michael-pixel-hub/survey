# Generated by Django 2.2.20 on 2021-06-27 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0018_auto_20210626_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='telegram_channel_id',
        ),
    ]