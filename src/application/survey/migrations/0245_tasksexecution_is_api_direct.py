# Generated by Django 2.2.28 on 2022-11-02 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0244_auto_20221102_0209'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksexecution',
            name='is_api_direct',
            field=models.BooleanField(blank=True, null=True, verbose_name='Напрямую через API'),
        ),
    ]
