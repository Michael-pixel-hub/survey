# Generated by Django 2.2.28 on 2022-11-02 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0242_userdevice_os_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksexecution',
            name='is_fake_gps',
            field=models.BooleanField(blank=True, null=True, verbose_name='Inspector is work'),
        ),
    ]
