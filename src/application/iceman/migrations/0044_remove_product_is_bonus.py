# Generated by Django 2.2.24 on 2022-02-23 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('iceman', '0043_source_online_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_bonus',
        ),
    ]
