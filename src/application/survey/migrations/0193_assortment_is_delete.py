# Generated by Django 2.2.24 on 2022-04-09 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0192_task_assortment_1c'),
    ]

    operations = [
        migrations.AddField(
            model_name='assortment',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='Delete'),
        ),
    ]
