# Generated by Django 2.2.24 on 2022-04-11 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0193_assortment_is_delete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assortment_1c',
        ),
    ]
