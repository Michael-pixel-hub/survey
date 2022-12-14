# Generated by Django 2.2.20 on 2021-07-07 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0110_auto_20210707_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='taxpayer_bank_account',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bank account'),
        ),
        migrations.AddField(
            model_name='user',
            name='taxpayer_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='User name'),
        ),
        migrations.AddField(
            model_name='user',
            name='taxpayer_passport_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Passport number'),
        ),
        migrations.AddField(
            model_name='user',
            name='taxpayer_passport_series',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Passport series'),
        ),
        migrations.AddField(
            model_name='user',
            name='taxpayer_patronymic',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Patronymic'),
        ),
        migrations.AddField(
            model_name='user',
            name='taxpayer_surname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Surname'),
        ),
    ]
