# Generated by Django 2.2.28 on 2022-08-16 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0231_task_ai_project'),
        ('iceman', '0102_auto_20220629_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreTaskSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('per_week', models.IntegerField(blank=True, null=True, verbose_name='How many times a week')),
                ('per_month', models.IntegerField(blank=True, null=True, verbose_name='How many times a month')),
                ('days_of_week', models.CharField(blank=True, default='', max_length=100, verbose_name='Days of weeks')),
                ('is_once', models.BooleanField(blank=True, default=False, verbose_name='Execution once')),
                ('only_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='survey.User', verbose_name='Пользователь')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iceman.Store', verbose_name='Магазин')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Расписание задачи в магазине',
                'verbose_name_plural': 'Расписание задач',
                'db_table': 'iceman_stores_tasks_schedule',
                'ordering': ['task__name', 'store__name', 'id'],
            },
        ),
    ]