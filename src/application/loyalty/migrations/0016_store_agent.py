# Generated by Django 2.2.20 on 2021-06-16 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loyalty', '0015_department_telegram_channel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='agent',
            field=models.CharField(blank=True, default='', max_length=1000, verbose_name='Sales Representative'),
        ),
    ]