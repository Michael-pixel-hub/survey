# Generated by Django 2.2.28 on 2022-07-13 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0223_auto_20220713_1301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasksexecutionstep',
            options={'ordering': ['-task__date_start', 'date_start'], 'verbose_name': 'Шаг выполнения задачи', 'verbose_name_plural': 'Шаги выполнения задачи'},
        ),
        migrations.RemoveField(
            model_name='tasksexecutionstep',
            name='order',
        ),
    ]
