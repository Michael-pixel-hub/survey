# Generated by Django 2.2.24 on 2021-08-08 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0135_auto_20210808_1342'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tasksexecutionquestionnaire',
            unique_together={('name', 'task', 'constructor_step_name')},
        ),
    ]
