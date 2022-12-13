# Generated by Django 2.2.20 on 2021-06-30 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0091_auto_20210629_1453'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasksexecutionassortmentbefore',
            options={},
        ),
        migrations.AlterField(
            model_name='tasksexecutionassortmentbefore',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_tasksexecutionassortmentbefore_good', to='survey.Good', verbose_name='Good'),
        ),
        migrations.AlterField(
            model_name='tasksexecutionassortmentbefore',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_tasksexecutionassortmentbefore_task', to='survey.TasksExecution', verbose_name='Task execution'),
        ),
    ]