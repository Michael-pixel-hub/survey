# Generated by Django 2.2.24 on 2022-06-01 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0212_tasksexecutioncheckinspector'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasksexecutioncheck',
            options={'ordering': ['date_start'], 'verbose_name': 'Task execution check', 'verbose_name_plural': 'Tasks execution checks'},
        ),
        migrations.AlterModelOptions(
            name='tasksexecutioncheckinspector',
            options={'ordering': ['date_start'], 'verbose_name': 'Task execution', 'verbose_name_plural': 'Проверка причин не распозналось'},
        ),
    ]
