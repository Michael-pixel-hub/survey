# Generated by Django 2.2.24 on 2021-07-20 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0113_storetask_per_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='new_task',
            field=models.BooleanField(default=False, verbose_name='New task with constructor'),
        ),
    ]
