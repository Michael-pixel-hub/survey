# Generated by Django 2.1 on 2019-11-07 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0052_tasksexecution_telegram_channel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='storetask',
            name='telegram_channel_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Telegram channel id'),
        ),
    ]