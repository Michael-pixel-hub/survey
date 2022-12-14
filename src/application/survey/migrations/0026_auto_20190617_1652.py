# Generated by Django 2.1 on 2019-06-17 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0025_auto_20190613_1934'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasksexecutioncheck',
            options={'verbose_name': 'Task execution check', 'verbose_name_plural': 'Tasks execution checks'},
        ),
        migrations.AddField(
            model_name='task',
            name='is_parse',
            field=models.BooleanField(blank=True, default=False, verbose_name='Parse by inspector'),
        ),
    ]
