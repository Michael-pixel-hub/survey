# Generated by Django 2.2.24 on 2022-06-01 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0211_auto_20220531_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='TasksExecutionCheckInspector',
            fields=[
            ],
            options={
                'verbose_name': 'Task execution',
                'verbose_name_plural': 'Проверка причин не распозналось',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('survey.tasksexecution',),
        ),
    ]
