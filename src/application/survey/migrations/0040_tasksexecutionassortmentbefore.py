# Generated by Django 2.1 on 2019-07-26 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0039_tasksexecution_set_check_not_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='TasksExecutionAssortmentBefore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avail', models.FloatField(verbose_name='Avail')),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tea_good_b', to='survey.Good', verbose_name='Good')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tea_task_b', to='survey.TasksExecution', verbose_name='Task execution')),
            ],
            options={
                'verbose_name': 'Avail assortment',
                'verbose_name_plural': 'Avail assortments',
                'db_table': 'chl_tasks_executions_assortment_before',
                'ordering': ['-task__date_start', 'id'],
            },
        ),
    ]
