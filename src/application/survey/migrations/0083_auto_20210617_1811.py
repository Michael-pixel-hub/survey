# Generated by Django 2.2.20 on 2021-06-17 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0082_auto_20210616_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='taxpayer_passport_num',
        ),
        migrations.RemoveField(
            model_name='user',
            name='taxpayer_passport_series',
        ),
        migrations.AddField(
            model_name='user',
            name='taxpayer_passport',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Passport'),
        ),
    ]